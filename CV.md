# Jong-Yeol Na (나종열)

Robotics &amp; AI researcher — vision-language-action policies for surgical robotics,
and the perception stack that makes them trustworthy.

📧 [nagus1999@dgist.ac.kr](mailto:nagus1999@dgist.ac.kr) ·
💻 [github.com/Najongs](https://github.com/Najongs) ·
🔗 ORCID: `TODO` ·
📚 [Knowledge graph](https://najongs.github.io/knowledge-vault/)

> **채워 넣을 곳** — 현재 소속(학위과정·연구실·기간)과 ORCID 는 확인이 필요해 비워 두었습니다.
> `TODO` 를 검색해 채우시면 됩니다.

---

## Research Interests

**Vision-Language-Action policies** for medical robotics · **Robot pose estimation**
from vision foundation models · **Fiber-optic sensing** (EFPI / OCT) for instrument
state · **Sim-to-real transfer** and foundation policies for manipulation

---

## Education

| | |
|---|---|
| **TODO** — DGIST (Daegu Gyeongbuk Institute of Science and Technology) | `TODO`–present |
| *TODO: 학위과정 · 전공 · 지도교수* | |
| **B.S., Creative Convergence Engineering**, Hanbat National University, Daejeon | Mar. 2018 – `TODO` |
| Minor in Computer Engineering · Major GPA 3.8/4.5 · Cumulative GPA 3.55/4.5 | |

---

## Research Experience

**DGIST** — `TODO: 연구실명` `TODO`–present
- **Surgical needle-insertion VLA.** Vision-language-action policies for a Mecademic
  Meca500 R3 inserting a needle into an eye phantom. Two generations: a Qwen2.5-VL
  pipeline with fused OCT/FPI sensing, then a full reboot on LeRobot
  (SmolVLA / ACT / Diffusion Policy / π0) with a MuJoCo digital twin.
- **Monocular robot pose and joint-angle estimation.** Iterative model fitting on
  frozen DINOv3 features; the pipeline produces its own bounding box instead of taking
  one from ground truth, and recovers joint angles jointly with camera pose through
  differentiable forward kinematics. One configuration across every camera and both robots.
- **Fiber-optic instrument sensing.** EFPI interferometry and OCT for needle-tip state —
  phase unwrapping, layer detection, puncture-curve classification.
- **Bimanual foundation policies.** Curated a 16-DoF manipulation corpus (52 datasets,
  23,201 episodes, 10.3M frames) and the multi-GPU training pipeline that consumes it.

**Intelligent Big Data Lab**, Dept. of Creative Convergence Engineering,
Hanbat National University Sep. 2018 – `TODO`
- Machine learning for public-sector text: complaint classification, library demand
  analysis, recommender systems.

---

## Publications

**In preparation / under review**

1. **Jong-Yeol Na**, `TODO: 공저자`.
   *DINObotPose: Monocular Robot Pose and Joint Angle Estimation with a Pretrained
   Vision Foundation Model and Kinematic Fitting.*
   `TODO: venue / status` ·
   [code + weights](https://github.com/Najongs/DINObotPose) · `v1.0.0`

**Conference presentations**

2. **Jong-Yeol Na**\*, Min Jang, Se-jin Lim, Jung-o Kwon.
   *Automatic classification and prediction of complaints using machine learning.*
   KOTIS Spring Conference, May 2023. (oral)

---

## Patents

| | |
|---|---|
| Part-time job intermediary device technology (OwnLab) | Jun. 2022 |
| Personality evaluation evaluated by others | Jul. 2023 |

---

## Awards

| | |
|---|---|
| **National Student Big Data Analysis Competition** — *Automatic classification and prediction of complaints using machine learning* | Nov. 2022 |

---

## Entrepreneurship

**OwnLab** — founder Mar. 2022 – `TODO`
Initial Startup Package · I-Corps (public technology-based market-linked startup
exploration) · Hanbat University LINC+ Entrepreneurship Club ·
Data Voucher: part-time job review data production for small business owners

---

## Teaching &amp; Service

| | |
|---|---|
| Teaching Assistant, *Smart Engineering Design*, Hanbat National University | Spring 2022 |
| Yuseong-gu Youth Data-Based Problem Solving Group — civil complaint analysis | Spring 2022 |
| Yuseong-gu Youth Data-Based Problem Solving Group — public library book demand analysis | Spring 2023 |

---

## Training

| | |
|---|---|
| Seoul ICT Innovation Square — *AI Service Planning Process* | Aug. 2021 |
| Seoul ICT Innovation Square — *AI Advanced Language Intelligence Project Development* | Feb. 2022 |

---

## Technical Skills

**Languages** Python · C/C++ · CUDA · MATLAB
**ML** PyTorch · HuggingFace Transformers · LeRobot · timm · scikit-learn
**Robotics** ROS 2 · MuJoCo · NVIDIA Isaac Sim · differentiable forward kinematics
**Vision** OpenCV · DINOv2/v3 · SegFormer · SAM · ArUco / multi-camera calibration
**Hardware** Mecademic Meca500 R3 · Trossen WidowX AI (bimanual) · Pollen Reachy ·
FAIRINO FR5 · Franka · Stereolabs ZED · Luxonis OAK · EFPI / OCT fiber sensors
**Infrastructure** NVIDIA DGX-1 (8×V100) · multi-GPU training (`accelerate`, DDP/ZeRO) ·
uv / conda · Git

**Languages** Korean (native) · English (TOEIC 800)

---

## References

**TODO: 현재 지도교수**
`TODO`, DGIST

**Prof. Jun-Muck Lim** — former research supervisor
Intelligent Big Data Lab, Dept. of Creative Convergence Engineering,
Hanbat National University, Daejeon, South Korea ·
[jmlim@hanbat.ac.kr](mailto:jmlim@hanbat.ac.kr)

---

<sub>Last updated 2026-09-15 · plain-text source: [`CV.md`](CV.md)</sub>
