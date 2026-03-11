from finite_key import *

def _akl_worker(
        total_loss: list[float],
        angle: int,
        params: list[float],
        power: int
):
    ps = params.copy()
    ps[4] = params[4] * power

    qber, qx, m = neumann.raw_overpass(ps, total_loss)
    akl = (1-1.19*h(qber)-h(qx))/2 * m

    if akl > 0:
        return angle, power, akl
    return None

def power_akl_max_elev(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(30,91,1),
        power_range: np.ndarray = np.linspace(1,10,10),
        ax: typing.Optional[axes.Axes] = None,
        fontsize=16,
        tick_fontsize=12
    ) -> None:

    if ax is None:
        fig, ax = plt.subplots()

    ax.set_xlim(30,90)
    ax.grid(visible=True)

    filtered = []
    for prof in loss_profiles:
        angle = int(prof.name.split(' ')[-1].split('°')[0])
        if angle in max_elevation_range:
            filtered.append((prof.total_loss, angle))

    jobs = [
        (total_loss, angle, params, power)
        for (total_loss, angle) in filtered
        for power in power_range
    ]

    angles, pwrs, skls = [], [], []
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_akl_worker, *job) for job in jobs]
        for fut in as_completed(futures):
            res = fut.result()
            if res is None:
                continue
            angle, power, skl = res
            angles.append(angle)
            pwrs.append(power)
            skls.append(skl)

    ang_opt, pow_opt, akl_opt = optimal_power_curve(angles, pwrs, skls)
    cs = ax.tricontourf(
        angles,
        pwrs,
        skls,
        levels=[10, 100, 1000, 5000, 10000, 18000, 20000],
        norm=colors.LogNorm(),
        cmap='Purples'
    )
    ax.plot(
        ang_opt,
        pow_opt,
        linewidth=2,
        marker='.',
        linestyle='',
        color='red'
    )
    ax.tick_params(labelsize=tick_fontsize)
    ax.set_xticks(ticks=range(30, 91, 10))
    ax.set_yticks(ticks=range(0, 11, 2))

    cb = ax.figure.colorbar(
        mappable=cs,
        ax=ax,
        location='top',
        orientation='horizontal',
    )
    cb.ax.tick_params(labelsize=tick_fontsize)
    cb.ax.xaxis.set_ticks_position(position='top')
    cb.set_label(
        label='AKL (bits)',
        fontsize=fontsize
    )
    cb.ax.xaxis.set_label_position(position='top')

    last_x = ang_opt[-1]
    last_y = pow_opt[-1]
    ax.scatter(
        last_x,
        last_y,
        linewidth=24,
        marker='o',
        linestyle='',
        color='red',
        clip_on=False,
        zorder=10
    )
    ax.annotate(
        r'$P^\text{finite}_\text{opt}$',
        (last_x, last_y),
        xytext=(-40, 5),
        textcoords='offset points',
        color='red',
        fontsize=fontsize,
        ha='left',
        va='bottom'
    )

def _skl_worker(total_loss: list[float], angle: int, params: list[float], power: int):
    ps = params.copy()
    ps[4] = params[4] * power

    qber, qx, m = neumann.raw_overpass(ps, total_loss)
    m /= 2.0
    delta = (qber + qx) / 2.0

    skl = lim.smart_optimise(
        m=m,
        delta=delta,
        eps_qkd=1e-6,
        t=math.log2(10**8),
        f=1.19
    ) * m

    if skl > 0:
        return angle, power, skl
    return None

def power_skl_max_elev(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(30,91,1),
        power_range: np.ndarray = np.linspace(1,10,10),
        ax: typing.Optional[axes.Axes] = None,
        fontsize=16,
        tick_fontsize=12
    ) -> None:
    if ax is None:
        fig, ax = plt.subplots()
    
    ax.set_xlim(30,90)
    ax.grid(visible=True)
    ax.invert_xaxis()

    filtered = []
    for prof in loss_profiles:
        angle = int(prof.name.split(' ')[-1].split('°')[0])
        if angle in max_elevation_range:
            filtered.append((prof.total_loss, angle))

    jobs = [
        (total_loss, angle, params, power)
        for (total_loss, angle) in filtered
        for power in power_range
    ]

    angles, pwrs, skls = [], [], []

    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_skl_worker, *job) for job in jobs]
        for fut in as_completed(futures):
            res = fut.result()
            if res is None:
                continue
            angle, power, skl = res
            angles.append(angle)
            pwrs.append(power)
            skls.append(skl)
    
    ang_opt, pow_opt, skl_opt = optimal_power_curve(angles, pwrs, skls)
    cs = ax.tricontourf(
        angles,
        pwrs,
        skls,
        levels=[10, 100, 500,1000,3000,6000,10000],
        norm=colors.LogNorm(),
        cmap='Blues'
    )
    ax.plot(
        ang_opt,
        pow_opt,
        linewidth=2,
        marker='.',
        linestyle='',
        color='red'
    )
    ax.tick_params(labelsize=tick_fontsize)
    ax.set_xticks(ticks=range(30, 91, 10))
    ax.set_yticks(ticks=range(0, 11, 2))

    cb = ax.figure.colorbar(
        mappable=cs,
        ax=ax,
        location='top',
        orientation='horizontal',
    )
    cb.ax.tick_params(labelsize=tick_fontsize)
    cb.ax.xaxis.set_ticks_position(position='top')
    cb.set_label(
        label='SKL (bits)',
        fontsize=fontsize
    )
    cb.ax.xaxis.set_label_position(position='top')

    last_x = ang_opt[-1]
    last_y = pow_opt[-1]
    ax.scatter(
        last_x,
        last_y,
        linewidth=24,
        marker='o',
        linestyle='',
        color='red',
        clip_on=False,
        zorder=10
    )
    ax.annotate(
        r'$P^\text{asym}_\text{opt}$',
        (last_x, last_y),
        xytext=(0, 5),
        textcoords='offset points',
        color='red',
        fontsize=fontsize,
        ha='left',
        va='bottom'
    )


if __name__ == '__main__':
    data_dir = pathlib.Path.home().joinpath(
        'Heriot-Watt University Team Dropbox',
        'RES_EPS_EMQL',
        'projects',
        'Optical ground station',
        '__software__',
        'finite_key',
        # 'Projects',
        # 'Finite_key_data'
    ).resolve()

    fontsize = 16
    tick_fontsize = 14
    dpi = 300
    filename = 'paper_fig_3.pdf'

    loss_profile_dir = data_dir.joinpath('550000m_0m_0.25m').resolve()

    loss_profiles = get_loss_profiles(dir=loss_profile_dir)
    power_range = np.linspace(0.1, 10, 50)
    max_elevation_range = range(30,151,1)
    params = params_10km_fibre

    fig, ax = plt.subplots(
        nrows=1,ncols=2,
        dpi=dpi,
        constrained_layout=True
    )
    fig.supxlabel(
        t=r'$\phi_\text{max}$ (°)',
        fontsize=fontsize
    )
    fig.supylabel(
        t=r'Power, $P$ (mW)',
        fontsize=fontsize
    )
    ax[0].plot(90,6)

    power_akl_max_elev(
        loss_profiles=loss_profiles,
        params=params,
        max_elevation_range=max_elevation_range,
        power_range=power_range,
        ax=ax[0],
        # ax=ax,
        fontsize=fontsize,
        tick_fontsize=tick_fontsize
    )
    power_skl_max_elev(
        loss_profiles=loss_profiles,
        params=params,
        max_elevation_range=max_elevation_range,
        power_range=power_range,
        ax=ax[1],
        fontsize=fontsize,
        tick_fontsize=tick_fontsize
    )
    fig.savefig(fname=filename, dpi=dpi)
    # plt.show()