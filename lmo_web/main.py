import json
import warnings
from collections.abc import Mapping

import lmo  # noqa: F401
import numpy as np
from lmo.diagnostic import l_ratio_bounds
from scipy.stats import distributions

import plotly.graph_objects as go
import plotly.io as pio

import js
from pyodide.ffi import to_js as _to_js
from pyscript import when
from pyweb import pydom

from web_storage import local_storage


rv_continuous_frozen: type[object] = type(distributions.norm())

NUM_x = 1000
MIN_x = -10
MAX_x = 10
MAX_f = 10

COLOR_FONT = 'var(--bs-body-color)'
CONFIG = {
    'logging': 2,  # verbose, default (warn+err) is 1
    'displaylogo': False,
    'responsive': True,
    'doubleClick': 'reset',
    'scrollZoom': False,
    'showAxisDragHandles': False,
    'modeBarButtonsToRemove': ['zoom', 'zoomin', 'zoomout', 'autoscale', 'resetscale'],
    'modeBarButtonsToAdd': ['togglespikelines', 'togglehover']
}
LAYOUT = go.Layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    autotypenumbers='strict',
    hoverdistance=200,
    dragmode='pan',
    clickmode='none',
    margin=go.layout.Margin(
        t=0, # top
        r=0, # right
        b=1, # bottom
        l=1, # left (0 causes missing gridlines due to some bug)
    ),
)

TEX_L_STATS = r'''$
\begin{{align*}}
    \lambda^{{{0}}}_1 &= {1:.4g} \\
    \lambda^{{{0}}}_2 &= {2:.4g} \\
    \tau^{{{0}}}_3 &= {3:.4g} \\
    \tau^{{{0}}}_4 &= {4:.4g}
\end{{align*}}
$'''.strip()

RVS: Mapping[str, rv_continuous_frozen] = {}


# redirect warnings to the console
warnings.showwarning = lambda *a, file=None, **k: js.console.warn(warnings.formatwarning(*a, **k))


def to_js(data):
    if data is None or isinstance(data, (bool, int, float, str, bytes)):
        return data
    return _to_js(data, dict_converter=js.Object.fromEntries)


def fig_to_js(fig, config=None):
    data_json = fig.to_json(validate=False)
    if not config:
        return js.JSON.parse(data_json)

    if not isinstance(config, dict):
        raise TypeError(f'config must be a dict or None, got {type(config)}')

    data = json.loads(data_json)
    data['config'] = config
    return to_js(data)


def show_plot(fig, target='chart', config=CONFIG):
    # https://plotly.com/javascript/plotlyjs-function-reference/#plotlyreact
    return js.window.Plotly.react(target, fig_to_js(fig, config=config))


def init_state() -> None:
    if 'state' not in local_storage:
        local_storage['state'] = {
            'rv': [{
                'name': 'scipy.stats.norm',
                'params': [0.0, 1.0],
                'func': 'pdf',
            }],
        }


def init_rvs():
    # requires init_state()
    for attr in dir(distributions):
        if not attr.endswith('_gen'):
            continue

        name = attr[:-4]
        rv = getattr(distributions, name, None)

        # TODO: support rv's with shape params
        if rv._shape_info():
            continue

        # TODO: support discrete rv's
        if not hasattr(rv, 'pdf'):
            continue

        RVS[f'scipy.stats.{name}'] = rv

    # TODO: lmo distributions (requires support for shape params)

    for select, rv_state in zip(pydom['.select-rv'], local_storage['state']['rv']):
        name_selected = rv_state['name']
        for name in sorted(RVS):
            option = pydom.create('option')
            option.value = name
            option.html = name
            if name == name_selected:
                option.selected = True
            select.append(option)


def init_funcs():
    funcs = ['pdf', 'cdf']
    for select, rv_state in zip(pydom['.select-func'], local_storage['state']['rv']):
        func_selected = rv_state['func']
        for func in funcs:
            option = pydom.create('option')
            option.value = func
            option.html = func
            if func == func_selected:
                option.selected = True
            select.append(option)


def init_panel():
    # remove the placeholders
    spinner = pydom['#rv_placeholders'][0]
    spinner.remove_class('d-flex')
    spinner.add_class('d-none')

    # display the rv panel
    pydom['#rv'][0].remove_class('d-none')



def plotting_positions(X: rv_continuous_frozen, n: int = NUM_x):
    a, b = X.support()
    lb, ub = np.isfinite(a), np.isfinite(b)

    if lb and ub:
        # finite support: [5%, 90%, 5%] split as 1:2:1
        p_body = np.linspace(.05, .95, n - 2 * (n // 4))
        x_body = X.ppf(p_body)
        x_tail_a = np.linspace(a, x_body[0], n // 4, endpoint=False)
        x_tail_b = np.linspace(b, x_body[-1], n // 4, endpoint=False)[::-1]
        return np.r_[x_tail_a, x_body, x_tail_b]
    if lb:
        # left-bound: [20%, 80%) split as 1:9
        p_tail = np.linspace(.2, 1 - 1 / n**2, n - n // 10)
        x_tail = X.ppf(p_tail)
        x_body = np.linspace(a, x_tail[0], n // 10, endpoint=False)
        return np.r_[x_body, x_tail]
    if ub:
        # right-bound: (80%, 20%] split as 9:1
        p_tail = np.linspace(1 / n**2, .8, n - n // 10)
        x_tail = X.ppf(p_tail)
        x_body = np.linspace(b, x_tail[-1], n // 10, endpoint=False)[::-1]
        return np.r_[x_tail, x_body]

    # unbound: (99%, 99%) split as 1:8:1
    p_body = np.linspace(.01, .99, n - 2 * (n // 10))
    x_body = X.ppf(p_body)
    x_tail_a = np.linspace(X.ppf(1 / n**2), x_body[0], n // 10, endpoint=False)
    x_tail_b = np.linspace(X.ppf(1 - 1 / n**2), x_body[-1], n // 10, endpoint=False)[::-1]
    return np.r_[x_tail_a, x_body, x_tail_b]


def check_l_stats(l_stats, trim=(0, 0)):
    if l_stats[1] <= 0 or not np.all(np.isfinite(l_stats)):
        return False

    t_min, t_max = l_ratio_bounds(np.arange(3, len(l_stats) + 1), trim=trim)
    t = l_stats[2:]
    return np.all((t >= t_min) & (t <= t_max))


def _annotate_l_stats(X: rv_continuous_frozen, fig, trim=(0, 0)):
    *_, loc, scale = X.args
    lb, ub = np.isfinite(X.support())

    if np.array(trim).ndim == 0:
        trim = trim, trim

    assert len(trim) == 2
    if trim == (0, 0) and not np.isfinite(X.mean()):
        assert not (lb and ub)
        trim = 1 - int(lb), 1 - int(ub)

    if X.dist.name == 'wald':
        # workaround for `scipy.stats.wald`, see:
        # https://github.com/jorenham/Lmo/issues/142
        l_stats = [np.nan] * 4
    else:
        l_stats = X.l_stats(trim=trim)

        # find the minimum trim that result in valid L-stats
        # increment trim on the unbounded side(s) until valid L-stats
        while (
            abs(l_stats[2]) >= 1 or abs(l_stats[3]) >= 1
            or not check_l_stats(l_stats, trim)
        ):
            assert not (lb and ub) and max(trim) < 100

            # if lb and trim[0] >= 1:
            #     trim = trim[0] - 1, trim[1]
            # elif ub and trim[1] >= 1:
            #     trim = trim[0], trim[1] - 1
            # elif ub and lb and trim[0] != trim[1]:
            #     trim = min(trim), min(trim)
            trim = trim[0] + 1 - int(lb), trim[1] + 1 - int(ub)

            l_stats = X.l_stats(trim=trim)

    if trim == (0, 0):
        trim_str = ''
        l_prefix = 'L'
    elif trim[0] == trim[1]:
        trim_str = f'({trim[0]:.2g})'
        l_prefix = 'TL'
    else:
        trim_str = f'({trim[0]:.2g}, {trim[1]:.2g})'
        if trim[0] == 0:
            l_prefix = 'LL'
        elif trim[1] == 0:
            l_prefix = 'LH'
        else:
            l_prefix = 'generalized TL'

    fig.add_annotation(
        text=(
            TEX_L_STATS
            .format(trim_str, *l_stats)
            .replace('nan', r'\text{indeterminate}')
            .replace('inf', r'\inf')
        ),
        xref='paper',
        yref='paper',
        xanchor='right',
        yanchor='top',
        x=1,
        y=1,
        xshift=-16,
        yshift=-32,
        showarrow=False,
        hovertext=f'{l_prefix}-moments',
        font_size=24,
    )


def get_rv(i: int) -> rv_continuous_frozen:
    rv_state = local_storage['state']['rv'][i]
    args = rv_state['params']
    return RVS[rv_state['name']](*args)


def update_rv_state(i: int, **kwds):
    # mutating local_storage['state'] is just a dict; updating it
    # won't magically update thte local storage
    state_dict = local_storage['state']
    state_dict['rv'][i] |= kwds

    # save to local storage
    local_storage['state'] = state_dict


def update_plot(i: int):
    if i != 0:
        raise NotADirectoryError('multiple RV\'s not supported')

    X = get_rv(i)

    # get the plotting positions
    x = plotting_positions(X)

    # plot the PDF or CDF

    func = local_storage['state']['rv'][i]['func']
    if func == 'pdf':
        y = X.pdf(x)
        fname = '$f(x)$'
        ymax = None
    elif func == 'cdf':
        y = X.cdf(x)
        fname = '$F(x)$'
        ymax = 1.01
    else:
        raise TypeError(func)

    fig = go.Figure(layout=LAYOUT)

    fig.add_trace(go.Scatter(
        x=x.tolist(),
        y=y.tolist(),
        fill='tozeroy',
        name=fname,
    ))

    a, b = X.support()
    lb, ub = np.isfinite(a), np.isfinite(b)

    # determine the "interesting" domain and range
    *_, loc, scale = X.args
    x_min = a if lb else max(x[0], X.ppf(0.001), MIN_x * scale + loc)
    x_max = b if ub else min(x[-1], X.ppf(0.999), MAX_x * scale + loc)
    assert x_min < x_max

    minor_layout = {
        'showgrid': True,
        'ticks': '',
        'griddash': 'dash',
        'gridwidth': 1
    }

    # x-axis
    fig.update_xaxes(
        type='linear',
        minor=minor_layout,
        gridwidth=2,
        ticks='',
        ticklabelposition='inside right',
        hoverformat=',.3r',
        range=[x_min, x_max],
        zeroline=True,
        zerolinewidth=2,
        fixedrange=bool(lb and ub),
        minallowed=x[0],
        maxallowed=x[-1],
    )

    # y-axis
    fig.update_yaxes(
        type='linear',
        minor=minor_layout,
        gridwidth=2,
        ticks='',
        ticklabelposition='inside top',
        hoverformat=',.3r',
        # range=[0, min(y.max() * 1.01, MAX_f)],
        range=[0, None],
        fixedrange=True,
        # minallowed=-0.01,
        minallowed=0,
    )

    _annotate_l_stats(X, fig)

    # add quantile annotations
    # ps = [1, 5, 25, 50, 75, 95, 99]
    # if lb:
    #     ps = ps[1:]
    # if ub:
    #     ps = ps[:-1]
    # qs = X.ppf(np.array(ps) / 100)
    # for p, q in zip(ps, qs):
    #     fig.add_annotation(
    #         text=f'{p}%',
    #         x=q,
    #         xref='x',
    #         y=0,
    #         yref='paper',
    #         showarrow=False,
    #     )

    # display the plot
    return show_plot(fig)


@when('change', '#rv .select-rv')
def on_rv_change(event):
    select = event.target

    rv_ix = int(select.id.split('_')[1])

    name_cur = local_storage['state']['rv'][rv_ix]['name']
    name_new = select.value

    if name_new == name_cur:
        return

    params_new = [0.0, 1.0]

    rv = RVS[name_new]
    if rv._shape_info():
        # TODO: initial shape param values;
        # see ._fitstart() or something
        raise NotImplementedError('shape parameters not supported')

    update_rv_state(rv_ix, name=name_new, params=params_new)
    update_plot(rv_ix)


@when('keydown', '#rv [contenteditable]')
def on_param_keydown(event):
    """Prevent non-numeric input, but allow special keys (with len > 1) to pass through."""
    # TODO: ArrowUp / ArrowDown for increment / decrement
    if len(event.key) == 1 and event.key not in '1234567890-+_.':
        event.preventDefault()


@when('input', '#rv [contenteditable]')
def on_param_input(event):
    # TODO: debounce; `onchange` event maybe?

    target = event.target
    id_ = target.id
    value_raw = target.innerText

    try:
        # TODO: integer input (see `rv._param_info()[param_ix].integral`)
        value = float(value_raw)
    except ValueError as e:
        # TODO: display error in the UI
        print(*e.args)
        return

    _, rv_ix_raw, _, param_ix_raw = id_.split('_')
    rv_ix = int(rv_ix_raw)

    param_ix = int(param_ix_raw)
    if param_ix == -1 and value <= 0:
        # scale must be positive
        # TODO: display error in the UI
        print(f'scale must be strictly positive, got {value}')
        return
    if param_ix >= 0 or param_ix < -2:
        # TODO: use rv._argcheck
        raise NotImplementedError('shape arguments')

    rv_state = local_storage['state']['rv'][rv_ix]
    params = rv_state['params']

    # rv = RVS[rv_state['name']]

    if len(params) != 2:
        assert len(params) > 2
        raise NotImplementedError('shape arguments')

    if params[param_ix] == value:
        # no change
        return

    params[param_ix] = value

    update_rv_state(rv_ix, params=params)
    update_plot(rv_ix)


@when('change', '#rv .select-func')
def on_func_change(event):
    select = event.target

    rv_ix = int(select.id.split('_')[1])

    func_cur = local_storage['state']['rv'][rv_ix]['func']
    func_new = select.value

    if func_new == func_cur:
        return
    if func_new not in {'pdf', 'cdf'}:
        raise NotImplementedError(f'func {func_new!r} not supported')

    update_rv_state(rv_ix, func=func_new)
    update_plot(rv_ix)


try:
    init_state()
    init_rvs()
    init_funcs()
    init_panel()

    update_plot(0)
except BaseException as e:
    import traceback
    tb = ''.join(traceback.TracebackException.from_exception(e).format())

    js.console.error(tb)
    js.document.body.innerHTML = f'<pre>{tb}</pre>'

    raise
