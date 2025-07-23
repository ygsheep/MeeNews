import os
import sys
import subprocess

if __name__ == '__main__':
    # 允许通过环境变量或命令行参数指定端口
    port = os.environ.get('PORT') or (sys.argv[1] if len(sys.argv) > 1 else '8090')
    print(f"[INFO] 启动Django开发服务器，端口: {port}")
    # 切换到server目录，启动Django
    os.chdir(os.path.join(os.path.dirname(__file__), 'server'))
    subprocess.run([sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}']) 