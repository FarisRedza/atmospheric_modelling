from finite_key import *

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
    filename = 'paper_fig_2.pdf'
    dpi = 300
    params = params_10km_fibre

    loss_profile_dir = data_dir.joinpath('up_link_passes').resolve()

    loss_profiles = get_loss_profiles(dir=loss_profile_dir)

    fig, ax = plt.subplots(
        nrows=2,ncols=1,
        dpi=dpi,
        constrained_layout=True
    )

    fig.supxlabel(
        t='Time (s)',
        fontsize=fontsize
    )
    fig.supylabel(
        t=r'$\phi_\text{max}$ (°)',
        fontsize=fontsize
    )

    fig_4(
        loss_profiles=loss_profiles,
        ax=ax[0],
        xlim=(-300,300)
    )
    fig_5(
        loss_profiles=loss_profiles,
        params=params,
        ax=ax[1],
        xlim=(-300,300),
        # xlabel='Time (s)'
    )
    fig.savefig(fname=filename, dpi=dpi)
    plt.show()