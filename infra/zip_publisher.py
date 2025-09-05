import os
import zipfile
import sys

# 루트 디렉토리에서만 제외할 디렉토리 및 파일
EXCLUDED_TOP_LEVEL_DIRS = {
    '.git', '.idea', '.venv', 'logs', 'uploads', 'build', 'dist'
}
EXCLUDED_TOP_LEVEL_FILES = {'.DS_Store'}

# 모든 위치에서 제외할 디렉토리
ALWAYS_EXCLUDED_DIRS = {'__pycache__'}

def zip_directory():
    try:
        script_path = os.path.abspath(sys.argv[0])
        script_name = os.path.basename(script_path)
        base_dir = os.path.dirname(script_path)

        # dist 디렉토리 생성
        dist_dir = os.path.join(base_dir, 'dist')
        os.makedirs(dist_dir, exist_ok=True)

        zip_path = os.path.join(dist_dir, 'publish.zip')

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(base_dir):
                rel_root = os.path.relpath(root, base_dir)

                # 모든 위치에서 __pycache__ 무조건 제외
                dirs[:] = [d for d in dirs if d not in ALWAYS_EXCLUDED_DIRS]

                # 루트 디렉토리일 경우 추가 필터 적용
                if rel_root == ".":
                    dirs[:] = [d for d in dirs if d not in EXCLUDED_TOP_LEVEL_DIRS]
                    files = [f for f in files if f not in EXCLUDED_TOP_LEVEL_FILES and f != script_name]
                else:
                    files = [f for f in files if f != script_name]

                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, base_dir)
                    zipf.write(file_path, rel_path)

        print(f"✅ Created zip: {zip_path}")

    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    zip_directory()
