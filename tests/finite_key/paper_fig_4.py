from finite_key import *

def _akl_worker(
        total_loss: list[float],
        dc: int,
        params: list[float],
        power: int
):
    ps = params.copy()
    ps[4] = params[4] * power

    qber, qx, m = neumann.raw_overpass(
        params=ps,
        loss_profile=total_loss,
        DC_B=dc
    )
    akl = (1-1.19*h(qber)-h(qx))/2 * m

    if akl > 0:
        return dc, power, akl
    return None

def power_akl_dc(
        loss_profile: LossProfile,
        params: list[float],
        dc_range: range,
        power_range: np.ndarray,
        ax: typing.Optional[axes.Axes] = None,
        fontsize=16,
        tick_fontsize=12
    ) -> None:

    if ax is None:
        fig, ax = plt.subplots()

    jobs = []
    for dc in dc_range:
        for power in power_range:
            jobs.append((loss_profile.total_loss, dc, params, power))

    dcs, pwrs, akls = [], [], []
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_akl_worker, *job) for job in jobs]
        for fut in as_completed(futures):
            res = fut.result()
            if res is None:
                continue
            dc, power, akl = res
            dcs.append(dc)
            pwrs.append(power)
            akls.append(akl)

    cs = ax.tricontourf(
        dcs,
        pwrs,
        akls,
        levels=[100,1000,10000,40000,100000],
        # levels=[1e1, 1e2, 1e3, 3e3, 6e3, 1e4, 3e4, 6e4, 1e5],
        norm=colors.LogNorm(),
        cmap='Purples'
    )

    # dc_opt, pow_opt, akl_opt = optimal_power_curve(dcs, pwrs, akls)
    # ax.plot(
    #     dc_opt,
    #     pow_opt,
    #     linewidth=2,
    #     marker='.',
    #     linestyle='',
    #     color='red'
    # )

    ax.tick_params(labelsize=tick_fontsize)
    ax.set_xlim(min(dc_range), max(dc_range))
    ax.set_xticks(ticks=range(min(dc_range), max(dc_range)+1, 100))
    ax.set_yticks(ticks=range(0, 11, 2))
    ax.grid(visible=True)

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

def _skl_worker(
        total_loss: list[float],
        dc: int,
        params: list[float],
        power: int
):
    ps = params.copy()
    ps[4] = params[4] * power

    qber, qx, m = neumann.raw_overpass(
        params=ps,
        loss_profile=total_loss,
        DC_B=dc
    )
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
        return dc, power, skl
    return None

def power_skl_dc(
        loss_profile: LossProfile,
        params: list[float],
        dc_range: range,
        power_range: np.ndarray,
        ax: typing.Optional[axes.Axes] = None,
        fontsize=16,
        tick_fontsize=12
    ) -> None:

    if ax is None:
        fig, ax = plt.subplots()

    jobs = []
    for dc in dc_range:
        for power in power_range:
            jobs.append((loss_profile.total_loss, dc, params, power))

    dcs, pwrs, skls = [], [], []
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_skl_worker, *job) for job in jobs]
        for fut in as_completed(futures):
            res = fut.result()
            if res is None:
                continue
            dc, power, skl = res
            dcs.append(dc)
            pwrs.append(power)
            skls.append(skl)

    cs = ax.tricontourf(
        dcs,
        pwrs,
        skls,
        levels=[100,1000,10000,40000,100000],
        # levels=[1e1, 1e2, 1e3, 3e3, 6e3, 1e4, 3e4, 6e4, 1e5],
        norm=colors.LogNorm(),
        cmap='Blues'
    )

    # dc_opt, pow_opt, skl_opt = optimal_power_curve(dcs, pwrs, skls)
    # ax.plot(
    #     dc_opt,
    #     pow_opt,
    #     linewidth=2,
    #     marker='.',
    #     linestyle='',
    #     color='red'
    # )

    ax.tick_params(labelsize=tick_fontsize)
    ax.set_xlim(min(dc_range), max(dc_range))
    ax.set_xticks(ticks=range(min(dc_range), max(dc_range)+1, 100))
    ax.set_yticks(ticks=range(0, 11, 2))
    ax.grid(visible=True)
    ax.invert_xaxis()

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
    filename = 'paper_fig_4.pdf'

    loss_profile_dir = data_dir.joinpath('550000m_0m_0.25m').resolve()

    loss_profiles = get_loss_profiles(dir=loss_profile_dir)
    loss_profile = get_loss_profile(
        max_elevation=90,
        loss_profiles=loss_profiles
    )
    power_range = np.linspace(0.1, 10, 20)
    # dc_range = range(200,1401,55)
    # params = params_no_fibre
    dc_range = range(0, 401, 10)
    params = params_10km_fibre

    fig, ax = plt.subplots(
        nrows=1,ncols=2,
        dpi=dpi,
        constrained_layout=True
    )
    fig.supxlabel(
        t='DC (cps)',
        fontsize=fontsize
    )
    fig.supylabel(
        t=r'Power, $P$ (mW)',
        fontsize=fontsize
    )

    power_akl_dc(
        loss_profile=loss_profile,
        params=params,
        dc_range=dc_range,
        power_range=power_range,
        ax=ax[0],
        fontsize=fontsize,
        tick_fontsize=tick_fontsize
    )
    power_skl_dc(
        loss_profile=loss_profile,
        params=params,
        dc_range=dc_range,
        power_range=power_range,
        ax=ax[1],
        fontsize=fontsize,
        tick_fontsize=tick_fontsize
    )
    fig.savefig(fname=filename, dpi=dpi)
    plt.show()