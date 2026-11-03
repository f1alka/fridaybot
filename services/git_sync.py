import git
import os
from loguru import logger
from config import settings

def sync_vault(commit_msg: str):
    """Git add, commit, push."""
    try:
        # Если репозиторий не инициализирован, инициализируем
        if not os.path.exists(os.path.join(settings.vault_path, ".git")):
            repo = git.Repo.init(settings.vault_path)
            if settings.git_repo_url:
                repo.create_remote("origin", settings.git_repo_url)
        else:
            repo = git.Repo(settings.vault_path)

        # Настройка автора
        with repo.config_writer() as cw:
            cw.set_value("user", "name", settings.git_user_name)
            cw.set_value("user", "email", settings.git_user_email)

        # Pull с rebase (чтобы избежать конфликтов)
        if settings.git_repo_url:
            try:
                repo.remotes.origin.pull(rebase=True)
            except Exception as e:
                logger.warning(f"Git pull failed (maybe empty repo): {e}")

        # Add & Commit
        repo.git.add(A=True)
        if repo.is_dirty():
            repo.index.commit(commit_msg)
            logger.info(f"Committed: {commit_msg}")
            
            # Push
            if settings.git_repo_url:
                repo.remotes.origin.push()
                logger.info("Pushed to remote")
                
    except Exception as e:
        logger.error(f"Git sync failed: {e}")