<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,12,20&height=160&section=header&text=Najongs&fontSize=58&fontAlignY=36&desc=robot%20learning%20·%20vision-language-action%20·%20surgical%20robotics&descAlignY=58&descSize=16&animation=fadeIn" />

**Robotics &amp; AI researcher.** I build vision-language-action policies for
surgical needle insertion, and the perception stack that makes them trustworthy.

</div>

---

## 🔬 What I work on

| | Area | Focus |
|---|---|---|
| 🪡 | **Vision-Language-Action** | Meca500 R3 + eye-phantom needle insertion. Two generations: a Qwen2.5-VL pipeline with fused OCT/FPI sensing, then a full reboot on LeRobot (SmolVLA · ACT · Diffusion · π0), plus a MuJoCo sim twin. |
| 🤖 | **Robot pose estimation** | Monocular and multi-view robot pose from a *frozen* DINO backbone — one set of weights across arms, no real-world training. Meca500 · FR5 · Franka · Baxter. |
| 🔦 | **Fiber-optic sensing** | EFPI interferometry and OCT for needle-tip state: phase unwrapping, layer detection, puncture-curve classification. |
| 🦾 | **Foundation policies** | Bimanual 16-DoF manipulation corpus — 52 datasets, 23k episodes, 10.3M frames — and the multi-GPU pipeline that trains on it. |

## 📚 Open knowledge graph

I keep my research as a **discourse graph** — every claim carries the evidence that
supports it, refuted approaches stay on the record, and open questions are first-class
nodes rather than TODOs.

### → **[najongs.github.io/knowledge-vault](https://najongs.github.io/knowledge-vault/)**

*Questions → Claims → Evidence → Experiments → Sources, rendered as a browsable graph.*

## 🧭 Selected repositories

**Vision-Language-Action**
[`Insertion_VLA`](https://github.com/Najongs/Insertion_VLA) ·
[`Insertion_VLAv2`](https://github.com/Najongs/Insertion_VLAv2) ·
[`Insertion_VLAv3`](https://github.com/Najongs/Insertion_VLAv3) ·
[`Insertion_VLA_Sim2`](https://github.com/Najongs/Insertion_VLA_Sim2) ·
[`Qwen2.5-VL-3B OCT/FPI`](https://github.com/Najongs/Qwen2.5-VL-3B-_OCT_FPI_Action_Model)

**Robot pose estimation**
[`DIP_ROBOTPOSE`](https://github.com/Najongs/DIP_ROBOTPOSE) ·
[`DINOv3_fine_tunning`](https://github.com/Najongs/DINOv3_fine_tunning) ·
[`DINObotPose3`](https://github.com/Najongs/DINObotPose3) ·
[`3d-robot-pose-estimation`](https://github.com/Najongs/3d-robot-pose-estimation) ·
[`Robot_joint_inference`](https://github.com/Najongs/Robot_joint_inference)

**Data collection &amp; calibration**
[`ZED_Cap_make_dataset`](https://github.com/Najongs/ZED_Cap_make_dataset) ·
[`Panda_cap_make_dataset`](https://github.com/Najongs/Panda_cap_make_dataset) ·
[`VLA_make_the_dataset`](https://github.com/Najongs/VLA_make_the_dataset) ·
[`Intertek_Zed_ArUco_Calibration`](https://github.com/Najongs/Intertek_Zed_ArUco_Calibration)

**Robot platforms**
[`reachy2019`](https://github.com/Najongs/reachy2019) ·
[`Albabot`](https://github.com/Najongs/Albabot) ·
[`Kiosk_pose_OnLab`](https://github.com/Najongs/Kiosk_pose_OnLab)

> Older repositories are **archived, not deleted** — a superseded approach is still a
> result. Each generation keeps code that never made it into its successor.

## 🛠 Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![MuJoCo](https://img.shields.io/badge/MuJoCo-1A73E8?style=flat-square&logo=google&logoColor=white)
![ROS 2](https://img.shields.io/badge/ROS%202-22314E?style=flat-square&logo=ros&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

**Hardware I run on** — Mecademic Meca500 R3 · Trossen WidowX AI (bimanual) ·
Pollen Reachy · FAIRINO FR5 · Franka · Stereolabs ZED · NVIDIA DGX-1 (8×V100)

## 📫 Reach me

[![Email](https://img.shields.io/badge/nagus1999@dgist.ac.kr-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:nagus1999@dgist.ac.kr)

<!--
Najongs/Najongs — this README renders on the profile page.
-->
