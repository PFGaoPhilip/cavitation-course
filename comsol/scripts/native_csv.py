"""Read COMSOL table exports without confusing parameter columns and units."""
from pathlib import Path
import csv,re
import numpy as np

def read_table(path):
    path=Path(path); lines=path.read_text(encoding='utf-8-sig').splitlines()
    headers=[]; body=[]
    for line in lines:
        if line.startswith('% '):
            candidate=next(csv.reader([line[2:]]))
            if len(candidate)>4:headers=candidate
        elif line and not line.startswith('%'):body.append(line)
    data=np.array([[float(x) for x in row] for row in csv.reader(body)],dtype=float)
    if data.ndim!=2 or data.shape[1]!=len(headers):
        raise ValueError(f'{path.name}: header/data shape mismatch {len(headers)} {data.shape}')
    if not np.isfinite(data).all():raise ValueError(f'{path.name}: nonfinite native result')
    names=[re.sub(r'\s+\(.*\)$','',h).strip() for h in headers]
    return headers,names,data

def column(table,expression):
    _,names,data=table
    indices=[i for i,h in enumerate(names) if h==expression]
    if not indices:raise KeyError(f'No {expression}: {names}')
    # Explicit expression columns follow auto-added display-unit parameter columns.
    return data[:,indices[-1]]
