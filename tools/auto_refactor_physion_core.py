import pathlib, subprocess

def run(cmd):
    print(f"[AUTO] {cmd}")
    subprocess.run(cmd, shell=True, check=False)

def main():
    run("autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r physion_core")
    run("isort physion_core")
    run("black physion_core")
    run("autopep8 --in-place --aggressive --aggressive -r physion_core")
    run("flake8 physion_core")
    run("pylint $(git ls-files 'physion_core/**/*.py') || true")
    run("pytest -q")

if __name__ == "__main__":
    main()
