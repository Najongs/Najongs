<div align="center">

<img src="assets/header.svg" alt="Jongyeol Na — Researcher, KIRO — AI Task Intelligence" width="100%" />

M.S. from DGIST, [Intelligent Robot OptoMechatronics (IROM) Lab](https://sites.google.com/view/dgist-irom/home).
I build vision-language-action policies for precision robot manipulation — and the sensing
stack that makes them trustworthy, because vision alone cannot tell you what a needle is
touching.

[![CV](https://img.shields.io/badge/CV-0b5394?style=flat-square&logo=readthedocs&logoColor=white)](CV.md)
[![Portfolio](https://img.shields.io/badge/Portfolio-1f6f3f?style=flat-square&logo=readme&logoColor=white)](PORTFOLIO.md)
[![Knowledge graph](https://img.shields.io/badge/Knowledge%20graph-5c3a8c?style=flat-square&logo=obsidian&logoColor=white)](https://najongs.github.io/knowledge-vault/)

</div>

---

## 🔬 What I work on

| | Area | Focus |
|---|---|---|
| 🪡 | **Vision-Language-Action** | Meca500 R3 + eye-phantom needle insertion. Two generations: a Qwen3.5-VL (2B) pipeline with fused OCT/FPI sensing, then a full reboot on LeRobot (SmolVLA · ACT · Diffusion · π0), plus a MuJoCo sim twin. |
| 🤖 | **Robot pose estimation** | Monocular and multi-view robot pose from a *frozen* DINO backbone — one set of weights across arms, no real-world training. Meca500 · FR5 · Franka · Baxter. |
| 🔦 | **Fiber-optic sensing** | EFPI interferometry and OCT for needle-tip state: phase unwrapping, layer detection, puncture-curve classification. |
| 🦾 | **Foundation policies** | Bimanual 16-DoF manipulation corpus — 52 datasets, 23k episodes, 10.3M frames — and the multi-GPU pipeline that trains on it. |

**Recent** — *Precision enhancement of epidural force-sensing needle with machine learning*,
Int. J. Optomechatronics **20**(1) 2026 (SCIE) · first-author papers at **KRoC 2025** and
**IEIE 2025** · co-author at **IROS**. Full list in the [CV](CV.md).

## 📚 Open knowledge graph

I keep my research as a **discourse graph** — every claim carries the evidence that
supports it, refuted approaches stay on the record, and open questions are first-class
nodes rather than TODOs.

[![Research knowledge graph](assets/knowledge-graph.gif)](https://najongs.github.io/knowledge-vault/)

### → **[najongs.github.io/knowledge-vault](https://najongs.github.io/knowledge-vault/)** — browse it live

*Recorded from the live site.* Every dot is a question, claim, evidence item, experiment
or source; every line is a typed relation between them. Refuted claims stay on the record
rather than being deleted — so the same experiment does not get run twice.

On the site the same graph can be re-projected as a cube, a helix or islands, or re-laid
by semantic similarity instead of links.

**Click the graph to explore it live.**

## 🧭 Code

### → **[`DINObotPose`](https://github.com/Najongs/DINObotPose)** `v1.0.0`

Monocular robot pose and joint-angle estimation with a pretrained vision foundation model
and kinematic fitting. Pinned dependencies, checkpoint SHA-256 manifest, environment
doctor, and one-command paper reproduction.

*The rest of my research repositories are private while the work is unpublished* —
VLA policies for needle insertion, the pose-estimation lineage, fibre-optic sensing,
and the data-collection and calibration tooling behind them. They open as the
corresponding papers do. The [portfolio](PORTFOLIO.md) describes what is in them.

> Superseded generations are **archived, not deleted** — a refuted approach is still a
> result, and each generation holds code that never made it into its successor.

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

[![KIRO](https://img.shields.io/badge/nagus1999@kiro.re.kr-0b5394?style=flat-square&logo=maildotru&logoColor=white)](mailto:nagus1999@kiro.re.kr)
[![DGIST](https://img.shields.io/badge/nagus1999@dgist.ac.kr-8a8a8a?style=flat-square&logo=gmail&logoColor=white)](mailto:nagus1999@dgist.ac.kr)

<!--
Najongs/Najongs — this README renders on the profile page.
-->
