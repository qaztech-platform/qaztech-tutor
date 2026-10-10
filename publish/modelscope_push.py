import os
from modelscope.hub.api import HubApi
R = "qaztechplatform/QAZTECH-Tutor-8B"; T = os.path.expanduser("~/.ms_token")
api = HubApi(); api.login(open(T).read().strip())
try:
    api.create_repo(R, repo_type="model", visibility="public", exist_ok=True); print("РЕПОЗИТОРИЙ ГОТОВ")
except Exception as e1:
    try: api.create_model(model_id=R, visibility=5, license="Apache License 2.0"); print("РЕПОЗИТОРИЙ СОЗДАН")
    except Exception as e2: print("СОЗДАНИЕ:", repr(e1)[:200], "|", repr(e2)[:200])
api.upload_folder(repo_id=R, folder_path=os.path.expanduser("~/tutor/ms_upload"), commit_message="QAZTECH Tutor 8B v0.2 preview")
os.remove(T); print("MODELSCOPE ЗАГРУЗКА ЗАВЕРШЕНА")
