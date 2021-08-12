import typer
from jobs import get_private_group_id_job, filter_fx_nv_job, forward_bot,filter_healer

app = typer.Typer()

@app.command()
def get_private_job_id(dialog_name: str):
    get_private_group_id_job.run(dialog_name=dialog_name)

@app.command()
def filter_fx_nv():
    filter_fx_nv_job.run()
@app.command()
def fw_bot():
     forward_bot.run()

@app.command()
def fw_healer():
     filter_healer.run()


if __name__ == "__main__":
    app()