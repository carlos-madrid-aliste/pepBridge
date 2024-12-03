from setuptools import setup, find_packages

setup(
    name="pepBridge",
    version="1.0.40",
    author="Carlos Madrid",
    author_email="creggae@gmail.com",
    description="A Python package for MALDI and LCMS data matching.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/carlos-madrid-aliste/pepBridge",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        "pepBridge": ["data/*.csv", "config_files/*.ini", "class_diagrams/*.png"],  
    },
    # Add this entry to specify where to install the script
    # The entry_points section defines the command line entry point for the script. 
    # In this case, the pepbridge command will call the main() function in 
    # pepBridge/bin/pepbridge.py.
    # The script will be installed in the bin directory of your virtual environment or 
    # system-wide if you use pip.
    #This configuration tells Python:
    #
    # pepbridge: The command users will type in the terminal.
    # pepBridge.bin.pepbridge:main: The module and function (main) to execute 
    entry_points={
        'console_scripts': [
        'pepbridge = pepBridge.bin.pepbridge:main',       # Main script
        'copy_data = pepBridge.bin.copy_data:copy_files',  # Script to copy data and config files
    ],
    
    },
)
