#!/usr/bin/env python3
"""
start_services.py

This script starts the Supabase stack first, waits for it to initialize, and then starts
the local AI stack. Both stacks use the same Docker Compose project name ("localai")
so they appear together in Docker.
"""

import os
import subprocess
import shutil
import time
import argparse
import platform
import sys
import subprocess

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        print("Supabase repository already exists, updating...")
        os.chdir("supabase")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in supabase/docker...")
    shutil.copyfile(env_example_path, env_path)

def stop_existing_containers():
    print("Stopping and removing existing containers for the unified project 'localai'...")
    cmd = ["docker", "compose", "-p", "localai"]
    cmd.extend(["-f", "docker-compose.yml", "down"])
    run_command(cmd)

def start_supabase():
    """Start the Supabase services (using its compose file)."""
    print("Starting Supabase services...")
    cmd = ["docker", "compose", "-p", "localai", "-f", "supabase/docker/docker-compose.yml"]   
    cmd.extend(["up", "-d"])
    run_command(cmd)

def start_local_ai(profiles=None):
    """Start the local AI services (using its compose file)."""
    print("Starting local AI services...")
    cmd = ["docker", "compose", "-p", "localai"]
    if profiles:
        for profile in profiles:
            cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml", "up", "-d"])
    run_command(cmd)

def main():
    parser = argparse.ArgumentParser(description='Start the local AI and Supabase services.')
    parser.add_argument('--profile', action='append', dest='profiles',
                      help='Profile to enable (can be specified multiple times)')
    parser.add_argument('--enable-supabase', action='store_true',
                      help='Enable Supabase service')

    args = parser.parse_args()

    # Only clone and prepare Supabase if it's enabled
    if args.enable_supabase:
        clone_supabase_repo()
        prepare_supabase_env()

    stop_existing_containers()

    # Start Supabase first if enabled
    if args.enable_supabase:
        start_supabase()
        # Give Supabase some time to initialize
        print("Waiting for Supabase to initialize...")
        time.sleep(10)

    # Then start the local AI services
    start_local_ai(profiles=args.profiles)

if __name__ == "__main__":
    main()
