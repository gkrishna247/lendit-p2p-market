# Updating Your Site (Future Changes)

Whenever you push new code to GitHub, run these on PythonAnywhere Bash:

```bash
workon lendit-env
cd /home/gkrishna247/lendit-p2p-market
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then go to the **Web** tab and click **Reload**. Your changes will be live within seconds.
