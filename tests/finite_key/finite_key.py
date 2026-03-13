import pathlib
import csv
import re
import dataclasses
import typing
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.axes as axes
import matplotlib.colors as colors

import lim
import neumann

params_no_fibre = [7.761328918344407, 7.542259886343475, 0.0335677812551474, 0.02531375770896907, 10826895.017621633, 4e-10]
params_10km_fibre = [9.47893858965945, 9.89101987420694, 0.037228590019520497, 0.03834132110856429, 6135831.8248959305, 1e-09]

max_workers = 6

@dataclasses.dataclass
class LossProfile:
    name: str
    time: list[float]
    atmospheric: list[float]
    diffraction: list[float]
    elevation: list[float]
    distance: list[float]

    @property
    def total_loss(self) -> list[float]:
        return [
            self.atmospheric[i]+self.diffraction[i]
            for i in range(len(self.atmospheric))
        ]

    @property
    def max_elevation(self) -> float:
        max_elev = float(self.name.split(' ')[-1].strip('°').strip())
        return max_elev

def h(x: float) -> float:
    return -x*np.log2(x)-(1-x)*np.log2(1-x)

def pixel(x: int) -> int:
    return x/plt.rcParams['figure.dpi']

def atoi(text: str) -> int | str:
    return int(text) if text.isdigit() else text

def natural_keys(text: str) -> list:
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def get_loss_profiles(dir: pathlib.Path) -> list[LossProfile]:
    file_strings = sorted(
        [str(s) for s in dir.iterdir()],
        key=natural_keys
    )
    loss_profile_files = [pathlib.Path(f) for f in file_strings]

    loss_profiles: list[LossProfile] = []
    for file in loss_profile_files:
        max_elevation = str(
            file.stem.split('_')[-1].split('degrees')[0]
        )
        name = f'Max elevation: {max_elevation}°'
        with open(file=file, mode='r') as csvfile:
            csvreader = csv.DictReader(f=csvfile, delimiter=',')
            headers = list(next(csvreader).keys())

            time: list[float] = []
            atmospheric: list[float] = []
            diffraction: list[float] = []
            elevation: list[float] = []
            distance: list[float] = []
            for row in csvreader:
                time.append(float(row[headers[0]]))
                atmospheric.append(float(row[headers[1]]))
                diffraction.append(float(row[headers[2]]))
                elevation.append(float(row[headers[3]]))
                distance.append(float(row[headers[4]]))
            
            loss_profiles.append(
                LossProfile(
                    name=name,
                    time=time,
                    atmospheric=atmospheric,
                    diffraction=diffraction,
                    elevation=elevation,
                    distance=distance
                )
            )
    return loss_profiles

def get_loss_profile(max_elevation: int, loss_profiles: list[LossProfile]) -> LossProfile:
    for l in loss_profiles:
        if int(l.name.split(' ')[-1].split('°')[0]) == max_elevation:
            return l
    raise ValueError('No matching loss profile')

def fig_1(
        loss_profiles: list[LossProfile],
        params_list: list[tuple[str, list[float]]],
        max_elevation_range: range = range(30,91),
        ax: typing.Optional[axes.Axes] = None
    ) -> None:
    '''
    Secret key length against max elevation

    fig_1(
        loss_profiles=loss_profiles,
        params_list=[
            ('10km fibre',params_10km_fibre),
            ('0km fibre',params_no_fibre)
        ]
    )
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.set_xlabel('Max elevation [Degrees]')
    ax.set_ylabel('Secret finite key length [bits]')
    ax.set_yscale('log')

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    for name, params in params_list:
        skl = []
        for loss_profile in loss_profiles:
            qber, qx, m = neumann.raw_overpass(
                params=params,
                loss_profile=[
                    loss_profile.atmospheric[i]+loss_profile.diffraction[i]
                    for i in range(len(loss_profile.atmospheric))
                ]
            )
            delta = (qber+qx)/2
            skl+=[lim.smart_optimise(
                m=m,
                delta=delta,
                eps_qkd=1e-6,
                t=np.log2(10**8),
                f=1.19
            )*m]
        skl += skl[::-1][1:]

        ax.plot(
            range(30,len(skl)+30),
            skl,
            label=name
        )
    ax.legend()

def fig_2(
        loss_profiles: list[LossProfile],
        max_elevation_range: range = range(30,91),
        ax: typing.Optional[axes.Axes] = None
) -> None:
    '''
    Raw key length against max elevation angle

    fig_2(
        loss_profiles=loss_profiles,
        max_elevation_range=range(5,91)
    )
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.set_xlabel(xlabel='Max elevation angle [Degrees]')
    ax.set_ylabel(ylabel='Raw key length (bits)')
    ax.set_yscale(value='log')

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    ms = []
    params = [9.47893858965945, 9.89101987420694, 0.037228590019520497, 0.03834132110856429, 6135831.8248959305, 1e-09]
    for loss_profile in loss_profiles:
        loss = [
            loss_profile.atmospheric[i]+loss_profile.diffraction[i]
            for i in range(len(loss_profile.atmospheric))
        ]
        qber, qx, m = neumann.raw_overpass(
            params=params,
            loss_profile=loss,
        )
        ms+=[m]
    ax.plot(
        max_elevation_range,
        ms,
        label='10km fibre'
    )

    ms = []
    params = [7.761328918344407, 7.542259886343475, 0.0335677812551474, 0.02531375770896907, 10826895.017621633, 4e-10]
    for loss_profile in loss_profiles:
        loss = [
            loss_profile.atmospheric[i]+loss_profile.diffraction[i]
            for i in range(len(loss_profile.atmospheric))
        ]
        qber, qx, m = neumann.raw_overpass(
            params=params,
            loss_profile=loss,
        )
        ms+=[m]
    ax.plot(
        max_elevation_range,
        ms,
        label='0km fibre'
    )
    ax.legend()

def fig_3(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevations: list[int] = [85,75,65,55,35]
    ) -> None:
    '''
    
    fig_3(
        loss_profiles=loss_profiles,
        params=params_10km_fibre
    )
    '''
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax2.invert_yaxis()
    ax1.set_xlabel(xlabel='Time [s]')
    ax1.set_ylabel(ylabel='QBER [%]')
    ax2.set_ylabel(ylabel='Total uplink loss [dB]')
    ax1.set_xlim(-200, 200)
    ax1.set_ylim(0, 15)
    ax2.set_ylim(55, 30)

    lp = [
        get_loss_profile(
            max_elevation=i,
            loss_profiles=loss_profiles
        ) for i in max_elevations
    ]
    for loss_profile in lp:
        loss = [
            loss_profile.atmospheric[i]+loss_profile.diffraction[i]
            for i in range(len(loss_profile.atmospheric))
        ]
        qber, qx, m = neumann.raw_overpass_instant(
            params=params,
            loss_profile=loss
        )
        ax1.plot(
            loss_profile.time,
            qber*100,
            label=loss_profile.name
        )
        ax2.plot(
            loss_profile.time,
            loss
        )

    ax1.legend()

def fig_4(
        loss_profiles: list[LossProfile],
        max_elevation_range: range = range(30,91),
        ax: typing.Optional[axes.Axes] = None,
        xlim: typing.Optional[tuple[float, float]] = None,
        xlabel: typing.Optional[str] = None,
        fontsize: int = 16,
        tick_fontsize: int = 14
) -> None:
    '''
    Contour plot of channel loss as a function of maximum elevation angle
    '''
    if ax is None:
        fig, ax = plt.subplots()

    if xlabel:
        ax.set_xlabel(xlabel=xlabel, fontsize=16)
    # ax.set_ylabel(ylabel=r'$\phi_\text{max}$ (°)', fontsize=16)

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    X, Y = np.meshgrid(
        loss_profiles[np.argmax([np.array(l.time).shape[0] for l in loss_profiles])].time,
        max_elevation_range
    )
    Z_loss: list[np.ndarray] = []
    max_length = np.max([np.array(l.time).shape[0] for l in loss_profiles])
    for l in loss_profiles:
        buffer_length = (max_length - np.array(l.time).shape[0])//2
        if np.array(l.time).shape[0] % 2 == max_length % 2:
            Z_loss.append(
                np.pad(
                    array=np.array(l.atmospheric) + np.array(l.diffraction),
                    pad_width=(buffer_length, buffer_length),
                    mode='constant',
                    constant_values=np.nan
                )
            )
        else:
            Z_loss.append(
                np.pad(
                    array=np.array(l.atmospheric) + np.array(l.diffraction),
                    pad_width=(buffer_length+1, buffer_length),
                    mode='constant',
                    constant_values=np.nan
                )
            )
    contour_set = ax.contour(
        X,
        Y,
        Z_loss,
        levels=[45,50,55,60,70],
        colors='white'
    )
    filled_contour_set = ax.contourf(
        X,
        Y,
        Z_loss,
        levels=np.linspace(38,85,50),
        cmap='inferno_r'
    )
    cbar = ax.figure.colorbar(mappable=filled_contour_set)
    cbar.set_label(
        label='Loss (dB)',
        fontsize=fontsize,
    )
    cbar.ax.yaxis.set_major_formatter(
        ticker.FormatStrFormatter('%0.1f')
    )
    ax.clabel(
        CS=contour_set,
        colors='white'
    )
    ax.tick_params(labelsize=tick_fontsize)
    ax.set_yticks(ticks=range(30, 91, 10))
    ax.set_xticks(ticks=range(-300, 301, 100))

def fig_5(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(30,91),
        ax: typing.Optional[axes.Axes] = None,
        xlim: typing.Optional[tuple[float, float]] = None,
        xlabel: typing.Optional[str] = None,
        fontsize: int = 16,
        tick_fontsize: int = 14
) -> None:
    '''
    Contour plot of instantaneous QBER as a function of maximum elevation angle
    '''
    if ax is None:
        fig, ax = plt.subplots()

    if xlabel:
        ax.set_xlabel(xlabel=xlabel, fontsize=16)
    # ax.set_ylabel(ylabel=r'$\phi_\text{max}$ (°)', fontsize=16)

    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    X, Y = np.meshgrid(
        loss_profiles[np.argmax([np.array(l.time).shape[0] for l in loss_profiles])].time,
        max_elevation_range
    )
    Z_qber: list[np.ndarray] = []
    max_length = np.max([np.array(l.time).shape[0] for l in loss_profiles])
    for l in loss_profiles:
        buffer_length = (max_length - np.array(l.time).shape[0])//2
        if np.array(l.time).shape[0] % 2 == max_length % 2:
            Z_qber.append(
                np.pad(
                    array=neumann.raw_overpass_instant(
                        params=params,
                        loss_profile=np.array(l.atmospheric)+np.array(l.diffraction)
                    )[0],
                    pad_width=(buffer_length, buffer_length),
                    mode='constant',
                    constant_values=np.nan
                )
            )
        else:
            Z_qber.append(
                np.pad(
                    array=neumann.raw_overpass_instant(
                        params=params,
                        loss_profile=np.array(l.atmospheric)+np.array(l.diffraction)
                    )[0],
                    pad_width=(buffer_length+1, buffer_length),
                    mode='constant',
                    constant_values=np.nan
                )
            )
    contour_set = ax.contour(
        X,
        Y,
        Z_qber,
        levels=[0.11],
        colors='white'
    )
    filled_contour_set = ax.contourf(
        X,
        Y,
        Z_qber,
        levels=np.linspace(0,0.5,50),
        cmap='inferno_r'
    )
    cbar = ax.figure.colorbar(mappable=filled_contour_set)
    cbar.set_label(
        label='QBER',
        fontsize=16
    )
    cbar.ax.yaxis.set_major_formatter(
        ticker.FormatStrFormatter('%0.3f')
    )
    ax.clabel(
        CS=contour_set,
        colors='white'
    )
    ax.tick_params(labelsize=tick_fontsize)
    ax.set_yticks(ticks=range(30, 91, 10))
    ax.set_xticks(ticks=range(-300, 301, 100))

def fig_6(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(5,90,5),
        ax: typing.Optional[axes.Axes] = None
    ) -> None:
    '''
    fig_6(
        loss_profiles=loss_profiles,
        params=params_10km_fibre
    )
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.set_xlabel('Central integration window [s]')
    ax.set_ylabel('Secret finite key length [bits]')
    ax.set_yscale('log')

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    for i, loss_profile in enumerate(loss_profiles):
        E_b, E_p, m = neumann.raw_overpass_instant(
            params=params,
            loss_profile=[
                loss_profile.atmospheric[i]+loss_profile.diffraction[i]
                for i in range(len(loss_profile.atmospheric))
            ]
        )
        result = []
        for k in range(0,180,10):
            central_block = slice(
                k,
                len(loss_profile.time)-k
            )
            cc_m_overpass_inner = m[central_block]
            avg_qber_inner = np.sum(
                np.array(E_b[central_block])*np.array(cc_m_overpass_inner)
            )/np.sum(cc_m_overpass_inner)
            result += [
                    lim.smart_optimise(
                    m=np.sum(cc_m_overpass_inner),
                    delta=avg_qber_inner,
                    eps_qkd=1e-6,
                    t=np.log2(10**8),
                    f=1.19
                )*np.sum(cc_m_overpass_inner)
            ]
        ax.plot(
            range(0,180,10),
            result[::-1],
            label=f'Max elevation: {max_elevation_range[i]}°'
        )
    ax.legend()

def fig_7(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(5,90,5),
        ax: typing.Optional[axes.Axes] = None
    ) -> None:
    '''
    fig_7(
        loss_profiles=loss_profiles,
        params=params_no_fibre,
        max_elevation_range=range(25,90,10)
    )
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.set_xlabel('Central integration window [s]')
    ax.set_ylabel('Secret finite key length [bits]')
    ax.set_yscale('log')

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    for i, loss_profile in enumerate(loss_profiles):
        E_b, E_p, m = neumann.raw_overpass_instant(
            params=params,
            loss_profile=[
                loss_profile.atmospheric[i]+loss_profile.diffraction[i]
                for i in range(len(loss_profile.atmospheric))
            ]
        )
        max_t = int(len(loss_profile.time)/2)
        result = []
        for k in range(0,max_t,10):
            central_block = slice(
                int(len(loss_profile.time)/2)-k,
                int(len(loss_profile.time)/2)+k
            )
            cc_m_overpass_inner = m[central_block]
            avg_qber_inner = np.sum(
                np.array(E_b[central_block])*np.array(cc_m_overpass_inner)
            )/np.sum(cc_m_overpass_inner)
            result += [
                    lim.smart_optimise(
                    m=np.sum(cc_m_overpass_inner),
                    delta=avg_qber_inner,
                    eps_qkd=1e-6,
                    t=np.log2(10**8),
                    f=1.19
                )*np.sum(cc_m_overpass_inner)
            ]
        ax.plot(
            range(0,max_t,10),
            result,
            label=f'Max elevation: {max_elevation_range[i]}°'
        )
    ax.legend()

def fig_8(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(5,90,5),
        ax: typing.Optional[axes.Axes] = None
    ) -> None:
    '''
    fig_8(
        loss_profiles=loss_profiles,
        params=params_no_fibre,
        max_elevation_range=range(85,90,10)
    )
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.set_xlabel('Central integration window [s]')
    ax.set_ylabel('Secret finite key length [bits]')
    ax.set_yscale('log')

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    for i, loss_profile in enumerate(loss_profiles):
        E_b, E_p, m = neumann.raw_overpass_instant(
            params=params,
            loss_profile=[
                loss_profile.atmospheric[i]+loss_profile.diffraction[i]
                for i in range(len(loss_profile.atmospheric))
            ]
        )
        max_t = int(len(loss_profile.time)/2)
        result_single = []
        result_double = []
        for k in range(0,max_t,10):
            central_block = slice(
                int(len(loss_profile.time)/2)-k,
                int(len(loss_profile.time)/2)+k
            )
            cc_m_overpass_inner = m[central_block]
            avg_qber_inner = np.sum(
                np.array(E_b[central_block])*np.array(cc_m_overpass_inner)
            )/np.sum(cc_m_overpass_inner)
            result_single += [
                    lim.smart_optimise(
                    m=np.sum(cc_m_overpass_inner),
                    delta=avg_qber_inner,
                    eps_qkd=1e-6,
                    t=np.log2(10**8),
                    f=1.19
                )*np.sum(cc_m_overpass_inner)
            ]

            result_two = []
            for j in range(0,int(len(loss_profile.time)/2)-k,10):
                second_block = slice(
                    j,
                    int(len(loss_profile.time)/2)-k
                )
                cc_m_overpass_outer = m[second_block]
                avg_qber_outer = np.sum(
                    np.array(E_b[second_block])*np.array(cc_m_overpass_outer)
                )/np.sum(cc_m_overpass_outer)
                result_two += [
                    2*lim.smart_optimise(
                    m=2*np.sum(cc_m_overpass_outer),
                    delta=avg_qber_outer,
                    eps_qkd=1e-6,
                    t=np.log2(10**8),
                    f=1.19
                )*np.sum(cc_m_overpass_outer)
                ]
            result_double += [np.max(result_two)]
        ax.plot(
            range(0,max_t,10),
            result_single,
            label=f'Max elevation: {max_elevation_range[i]}° - Single window'
        )
        ax.plot(
            range(0,max_t,10),
            np.nan_to_num(np.array(result_double))+np.array(result_single),
            label=f'Max elevation: {max_elevation_range[i]}° - Double window'
        )
    ax.legend()

def fig_9(
        loss_profiles: list[LossProfile],
        params: list[float],
        max_elevation_range: range = range(5,90,5),
        ax: typing.Optional[axes.Axes] = None
    ) -> None:
    '''
    fig_9(
        loss_profiles=loss_profiles,
        params=params_10km_fibre,
        max_elevation_range=range(85,90,10)
    )
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Total uplink loss [dB]')
    ax.set_xlim(-200, 200)
    ax.set_ylim(55, 30)

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    for loss_profile in loss_profiles:
        ax.plot(
            loss_profile.time,
            [
                loss_profile.atmospheric[i]+loss_profile.diffraction[i]
                for i in range(len(loss_profile.atmospheric))
            ],
            label=loss_profile.name
        )
    ax.legend()

def fig_10(
        loss_profiles: list[LossProfile],
        params_list: list[tuple[str, list[float]]],
        max_elevation_range: range = range(30,91),
    ) -> None:
    '''
    fig_10(
        loss_profiles=loss_profiles,
        params_list=[
            ('10km fibre',params_10km_fibre),
            ('0km fibre',params_no_fibre)
        ]
    )
    '''
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Max elevation [Degrees]')
    ax1.set_ylabel('Secret finite key length [bits]')
    ax1.set_yscale('log')

    ax2 = ax1.twinx()
    ax2.set_ylabel(ylabel='P(θ)')

    loss_profiles = [
        loss_profile for loss_profile in loss_profiles
        if int(loss_profile.name.split(' ')[-1].split('°')[0])
        in max_elevation_range
    ]

    for name, params in params_list:
        skl = []
        for loss_profile in loss_profiles:
            qber, qx, m = neumann.raw_overpass(
                params=params,
                loss_profile=[
                    loss_profile.atmospheric[i]+loss_profile.diffraction[i]
                    for i in range(len(loss_profile.atmospheric))
                ]
            )
            delta = (qber+qx)/2
            skl+=[lim.smart_optimise(
                m=m,
                delta=delta,
                eps_qkd=1e-6,
                t=np.log2(10**8),
                f=1.19
            )*m]
        skl += skl[::-1][1:]
        skl = np.nan_to_num(np.array(skl))
        annual_key = np.trapezoid(
            y=skl*1/np.sin(np.deg2rad(range(30,2*len(max_elevation_range)+30-1)))**2/2/np.sqrt(3),
            x=range(30,2*len(max_elevation_range)+30-1)
        ) * 445.5

        ax1.plot(
            range(30,len(skl)+30),
            skl,
            label=f'{name} - {annual_key:.2e} bits/year'
        )

    p_theta: np.ndarray = (1/np.sin(np.deg2rad(max_elevation_range))**2/2/np.sqrt(3))
    p_theta_list: list[float] = p_theta.tolist()
    p_theta_list += p_theta_list[::-1][1:]
    ax2.plot(
        range(30,2*len(max_elevation_range)+30-1),
        p_theta_list,
        linestyle='--'
    )
    ax1.legend()


def optimal_power_curve(angles, pwrs, values):
    '''
    Given scattered (angle, power, value) samples, return arrays:
    (unique_angles_sorted, opt_power_for_each_angle, opt_value_for_each_angle)

    Only uses points where value is finite.
    '''
    by_angle = defaultdict(list)
    for a, p, v in zip(angles, pwrs, values):
        if v is None:
            continue
        if not np.isfinite(v):
            continue
        by_angle[int(a)].append((float(p), float(v)))

    ang_sorted = np.array(sorted(by_angle.keys()), dtype=int)
    opt_p = np.full_like(ang_sorted, np.nan, dtype=float)
    opt_v = np.full_like(ang_sorted, np.nan, dtype=float)

    for i, a in enumerate(ang_sorted):
        pts = by_angle[a]
        # pick power that maximises v
        p_best, v_best = max(pts, key=lambda t: t[1])
        opt_p[i] = p_best
        opt_v[i] = v_best

    return ang_sorted, opt_p, opt_v
