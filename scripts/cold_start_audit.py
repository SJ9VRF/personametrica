from __future__ import annotations
import json, os, subprocess, sys, tempfile, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(cmd,check=True):
    return subprocess.run(cmd,check=check,text=True,capture_output=True)

def main():
    t0=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='personametrica-clean-') as td:
        venv=Path(td)/'venv'
        subprocess.run([sys.executable,'-m','venv',str(venv)],check=True,stdout=subprocess.DEVNULL)
        py=venv/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        mode='stdlib-path-isolation'
        editable=False
        pip_probe=run([str(py),'-m','pip','--version'],check=False)
        if pip_probe.returncode != 0:
            run([str(py),'-m','ensurepip','--upgrade'],check=False)
            pip_probe=run([str(py),'-m','pip','--version'],check=False)
        if pip_probe.returncode == 0:
            inst=run([str(py),'-m','pip','install','--no-deps','--no-build-isolation','-e',str(ROOT)],check=False)
            if inst.returncode == 0:
                mode='editable-install --no-deps --no-build-isolation'
                editable=True
        if not editable:
            # A fresh interpreter with no inherited PYTHONPATH. Add only this checkout
            # via a .pth file, which still catches undeclared runtime dependencies and
            # package/import assumptions without pretending a wheel was built.
            code='import site, pathlib; print(site.getsitepackages()[0])'
            sitepk=Path(run([str(py),'-c',code]).stdout.strip())
            (sitepk/'personametrica_checkout.pth').write_text(str(ROOT)+'\n')
        env=os.environ.copy(); env.pop('PYTHONPATH',None)
        imp=subprocess.run([str(py),'-c','import personalagi, personalbench; print("imports-ok")'],check=True,text=True,capture_output=True,env=env)
        cli=subprocess.run([str(py),'-m','personalagi','demo'],check=True,text=True,capture_output=True,env=env)
        result={
            'status':'PASS','version':'4.1.0','elapsed_seconds':round(time.perf_counter()-t0,3),
            'python':str(py),'isolation_mode':mode,'editable_install_completed':editable,
            'pip_available_in_fresh_venv':pip_probe.returncode==0,'core_dependencies_declared':0,
            'checks':{'fresh_venv_created':True,'package_imports':imp.stdout.strip()=='imports-ok','module_cli_demo_exit_zero':True},
            'cli_output_tail':cli.stdout.strip().splitlines()[-8:],
            'boundary':('A real editable install was completed in the fresh venv.' if editable else 'This runtime did not provide a usable pip installation path, so the audit used a fresh venv plus one repository .pth entry; it proves isolated imports and CLI execution, not wheel/build-backend installation.')+' Full scientific reproduction is covered separately by scripts/reproduce.py.'
        }
    (ROOT/'data/cold_start_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines=['# Cold-start execution audit','', '**Status: PASS**','',
        'A newly created virtual environment was used with inherited `PYTHONPATH` removed. The package imports and module CLI were then executed from that clean interpreter.', '',
        f"- isolation mode: `{result['isolation_mode']}`",
        f"- editable install completed: {'YES' if editable else 'NO (environment tooling limitation)'}",
        '- `import personalagi, personalbench`: PASS','- `python -m personalagi demo`: PASS',
        f"- measured audit runtime in this environment: {result['elapsed_seconds']:.3f}s", '',
        'Boundary: '+result['boundary'],'']
    (ROOT/'reports/COLD_START_AUDIT.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
