from setuptools import setup
import sys
import os

if sys.platform == 'win32':
    try:
        import py2exe
    except ImportError:
        print("Please install py2exe: pip install py2exe")
        sys.exit(1)

# Convert SVG to ICO if needed
ico_path = "app_icon.ico"
if not os.path.exists(ico_path) and os.path.exists("app_icon.svg"):
    try:
        from cairosvg import svg2png
        from PIL import Image
        import io
        
        # Convert SVG to PNG in memory
        png_data = svg2png(url="app_icon.svg", output_width=256, output_height=256)
        
        # Convert PNG to ICO
        img = Image.open(io.BytesIO(png_data))
        img.save(ico_path)
        print(f"Created {ico_path} from app_icon.svg")
    except ImportError:
        print("Warning: Could not convert SVG to ICO. Please install cairosvg and pillow:")
        print("pip install cairosvg pillow")
        print("Using default icon instead.")
        ico_path = None

setup(
    name="TaskMaster Pro",
    version="1.1.0",
    description="A feature-rich task management application with eye-catching design and stickers",
    author="TaskMaster Team",
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
            'packages': ['json', 'datetime', 'random', 'os', 'sys'],
            'excludes': ['tkinter', 'unittest', 'email', 'http', 'xml', 'pydoc'],
            'optimize': 2,
        }
    },
    windows=[{
        'script': "main.py", 
        'icon_resources': [(1, ico_path)] if ico_path else [],
        'dest_base': "TaskMaster Pro",
        'copyright': "© 2023 TaskMaster Team",
        'version': "1.1.0",
        'company_name': "TaskMaster Team",
        'product_name': "TaskMaster Pro"
    }],
    zipfile=None,
    data_files=[
        ('', ['app_icon.svg', 'README.md', 'requirements.txt']),
    ],
    install_requires=[
        'PyQt5>=5.15.0',
    ],
)