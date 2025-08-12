#!/usr/bin/env bash
# build.sh
# Exit on error
set -o errexit

# --- Backend Build ---
echo "--- Building backend ---"
cd backend # <--- THIS IS THE CRITICAL CHANGE

# Install Python dependencies
pip install --upgrade pip # It's good practice to upgrade pip first
pip install -r requirements.txt

# Collect static files (for Django Admin)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# --- Frontend Build (if needed from one script, but render.yaml handles it separately) ---
# The frontend build is handled by its own service definition in render.yaml
# and does not need to be in this script.```

**The key change is the `cd backend` command.** This tells the script: "Move into the `backend` directory," and all subsequent commands (`pip install`, `python manage.py migrate`, etc.) will run from the correct location where `requirements.txt` and `manage.py` exist.

---

### Your Next Steps

1.  **Update the `build.sh` file** on your local computer with the new code provided above.
2.  **Commit and push this change** to your GitHub repository.
    ```bash
    git add build.sh
    git commit -m "FIX: Correct path for backend build script"
    git push
    ```
3.  **Trigger a New Deployment on Render:**
    *   Go to your Render Dashboard.
    *   Navigate to your `yaba-bingo-backend` service.
    *   Click the **"Manual Deploy"** button and select **"Deploy latest commit"**.

This will restart the build process using your fixed `build.sh` script, and it should now succeed.

The `[notice] A new release of pip is available...` message is just a friendly notification; it was not the cause of the build failure. My updated script includes the pip upgrade as a best practice.