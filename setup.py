from setuptools import setup, find_packages

# Users can install either onnxruntime (CPU) or onnxruntime-gpu (GPU) as needed.
# Here, we specify onnxruntime as the default, but recommend for NVIDIA-GPU users to uninstall "pip uninstall onnxruntime" and install onnxruntime-gpu.

setup(
    name="n7speech",
    version="0.1.0",
    description="Real-time and file-based Meitei speech recognition and phoneme conversion",
    author="Thokchom Dayananda",
    author_email="thokchomdayananda54@gmail.com",
    url="https://github.com/OmeshThokchom/N7Speech.git",
    packages=find_packages(),
    install_requires=[
        # Default to CPU version; GPU users should manually install onnxruntime-gpu
        "onnxruntime==1.17.0",
        "numpy",
        "librosa",
        "torch",
        "sounddevice"
    ],
    extras_require={
        "gpu": ["onnxruntime-gpu"]
    },
    python_requires=">=3.7",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
