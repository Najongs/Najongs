# Portfolio — Jong-Yeol Na

Four threads of work, each with the repositories that hold it.
Diagrams render natively on GitHub; no image assets required.

📧 [nagus1999@dgist.ac.kr](mailto:nagus1999@dgist.ac.kr) ·
📄 [CV](CV.md) ·
📚 [Knowledge graph](https://najongs.github.io/knowledge-vault/)

---

## 1 · DINObotPose — monocular robot pose &amp; joint angles

**Problem.** Recover the 6-DoF camera-to-robot transform *and* the joint angles from a
single RGB frame — with no encoder readings and no ground-truth bounding box.
Competing methods take the box from ground truth or an external detector; that makes
their numbers hard to compare and their pipelines hard to deploy.

**Approach.** Keypoints are read from a **frozen** DINOv3 backbone. A first pass fits the
whole frame, then *projects its own solved skeleton* to define the crop for a second
pass — so the pipeline produces the box it needs. An iterative fit then recovers joint
angles together with camera pose from those keypoints alone, minimising a robustly
weighted reprojection error through differentiable forward kinematics.

```mermaid
flowchart LR
    IMG["Single RGB frame"] --> BB["DINOv3 backbone<br/>(frozen)"]
    BB --> P1["Pass 1<br/>full-frame keypoints"]
    P1 --> FIT1["Iterative fit<br/>robust reprojection"]
    FIT1 --> SK["Solved skeleton"]
    SK -->|"project → own bbox"| CROP["Crop"]
    CROP --> BB2["Crop detector<br/>(last 4 blocks tuned)"]
    BB2 --> P2["Pass 2<br/>sub-pixel keypoints"]
    P2 --> FIT2["Iterative fit<br/>differentiable FK"]
    FIT2 --> OUT["6-DoF pose<br/>+ joint angles"]

    style BB fill:#1f3a5f,color:#fff
    style BB2 fill:#1f3a5f,color:#fff
    style OUT fill:#2d5016,color:#fff
    style SK fill:#5c3a00,color:#fff
```

No depth model is trained, no weights are updated on the evaluated data, and **one
configuration serves every camera and both robots**.

**Release.** [`DINObotPose`](https://github.com/Najongs/DINObotPose) `v1.0.0` —
pinned dependencies, checkpoint SHA-256 manifest, `doctor.py` environment check, and
`reproduce_paper.sh`. The backbone architecture config ships in-package, so inference
needs no HuggingFace access.

**Lineage.** [`DINObotPose-v1`](https://github.com/Najongs/DINObotPose-v1) →
[`DINObotPose2`](https://github.com/Najongs/DINObotPose2) (Fourier domain adaptation) →
[`DINObotPose3`](https://github.com/Najongs/DINObotPose3) →
[`DIP_ROBOTPOSE`](https://github.com/Najongs/DIP_ROBOTPOSE) (research tree) → release.
Earlier still: [`Robot_joint_inference`](https://github.com/Najongs/Robot_joint_inference)
(2024-12) solved the same problem with DH kinematics and coordinate regression.

---

## 2 · Needle-insertion VLA — two generations, one task

**Task.** A Meca500 R3 inserting a needle into an eye phantom, guided by vision and
language, with fibre-optic sensing at the tip.

The lineage is not a refactor chain — **v4 replaced the framework rather than absorbing
its predecessors.** Measured overlap between v3 and v4 is 3 files (3.2%), which is why
the earlier generations are kept rather than deleted: each holds code that never made
it forward.

```mermaid
flowchart TD
    subgraph REAL["real — physical robot"]
        Q["Qwen2.5-VL-3B<br/>+ OCT/FPI encoders<br/>2025.10"]
        V1["v1 — monolithic VLA<br/>5-view, regression/diffusion heads"]
        V2["v2 — modularised<br/>flow matching, sensor CLIP, state MAE"]
        V3["v3 — eval &amp; ablation suite<br/>(most mature Qwen-era analysis)"]
        V4["v4 — LeRobot reboot<br/>SmolVLA · ACT · Diffusion · π0"]
        Q --> V1 --> V2 --> V3
        V3 -.->|"framework swap<br/>3.2% file overlap"| V4
    end

    subgraph SIM["sim — MuJoCo digital twin"]
        S0["Sim_make_MECA<br/>STL assets, data generation"]
        S1["Sim1 — calibration,<br/>digital twin bridge"]
        S2["Sim2 — staged pipeline<br/>Sim / Dataset / TRAIN / Eval"]
        S0 --> S1 --> S2
    end

    V4 <-->|"sim ↔ real"| S2

    style V4 fill:#2d5016,color:#fff
    style S2 fill:#2d5016,color:#fff
    style Q fill:#5c3a00,color:#fff
```

**Repositories.**
[`Insertion_VLA`](https://github.com/Najongs/Insertion_VLA) ·
[`Insertion_VLAv2`](https://github.com/Najongs/Insertion_VLAv2) ·
[`Insertion_VLAv3`](https://github.com/Najongs/Insertion_VLAv3) ·
[`Insertion_VLA_Sim2`](https://github.com/Najongs/Insertion_VLA_Sim2) ·
[`Qwen2.5-VL-3B OCT/FPI`](https://github.com/Najongs/Qwen2.5-VL-3B-_OCT_FPI_Action_Model)

The dataset behind it — 1,281 episodes, 145 GB — is published as a LeRobot dataset with
a card that documents its schema traps (two image encodings, sensor-rate mismatch).

---

## 3 · Fibre-optic sensing — knowing where the tip is

Vision stops at the surface. An EFPI (extrinsic Fabry-Pérot interferometer) and OCT at
the needle tip report what happens *inside* the tissue, and the interesting signal lives
in the phase.

```mermaid
flowchart LR
    RAW["EFPI / OCT<br/>raw interferogram"] --> PS["Phase shift"]
    PS --> UW["Robust unwrapping<br/>threshold + dwell"]
    UW --> PC["Puncture curve"]
    PC --> CLS["Layer / status<br/>classification"]
    CLS --> ST["Tip state"]
    ST -.->|"fused as VLA input"| VLA["Insertion policy"]

    style RAW fill:#1f3a5f,color:#fff
    style ST fill:#2d5016,color:#fff
    style VLA fill:#5c3a00,color:#fff
```

Work splits cleanly: signal processing (phase unwrapping, OCT layer detection,
self-attention / state encoders) on one side, puncture-curve classification — CNN,
fine-tuned, and LSTM-ResNet variants — on the other.

---

## 4 · Bimanual foundation policies

A 16-DoF bimanual manipulation corpus and the pipeline that trains on it, running on
8×V100.

```mermaid
flowchart LR
    G["GIST release<br/>17 sets · 50%"] --> M["Manifest<br/>make_manifest.py"]
    K["Self-collected<br/>10 sets · 20%"] --> M
    H["Hub third-party<br/>25 sets · 30%"] --> M
    M --> A["Distribution audit<br/>corpus_distribution_audit.md"]
    A --> T["train_multi.py<br/>in-memory concat,<br/>no disk merge"]
    T --> GPU["accelerate · 8×V100"]
    GPU --> CK["Checkpoints"]

    style M fill:#1f3a5f,color:#fff
    style A fill:#8b0000,color:#fff
    style CK fill:#2d5016,color:#fff
```

**52 datasets · 23,201 episodes · 10,313,809 frames.** The audit step is the part worth
pointing at: it found that among the 16 action dimensions, **one axis — the left gripper —
was scaled 137× apart between datasets.** Training without normalising it makes that
axis uninterpretable, and nothing in the loss would have told you.

---

## How I keep research

Every claim carries the evidence that supports it; refuted approaches stay on the
record rather than being deleted; open questions are nodes, not TODOs.

```mermaid
flowchart LR
    Q(["Question"]) -.->|answered by| C(["Claim"])
    E(["Evidence"]) -->|supports| C
    E2(["Evidence"]) -->|opposes| C
    X(["Experiment"]) -->|tests| C
    C -->|cites| S(["Source"])
    C -->|supersedes| C2(["older Claim"])

    style C fill:#1f3a5f,color:#fff
    style E fill:#2d5016,color:#fff
    style E2 fill:#8b0000,color:#fff
    style C2 fill:#444,color:#fff
```

A public extract is browsable at
**[najongs.github.io/knowledge-vault](https://najongs.github.io/knowledge-vault/)**.

---

<sub>Last updated 2026-09-15 · source: [`PORTFOLIO.md`](PORTFOLIO.md)</sub>
