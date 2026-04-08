---
url: https://github.com/newton-physics/newton
keywords: physics-simulation, gpu-accelerated, nvidia-warp, robotics, differentiable-physics
oneliner: NVIDIA Warp上に構築されたGPU高速物理シミュレーションエンジンで、ロボティクス・シミュレーション研究者向け。
---

# Newton — GPU 物理シミュレーションエンジン

## これは何？

Newton は **NVIDIA Warp** をバックエンドとする **GPU ネイティブの物理シミュレーションエンジン**。Disney Research・Google DeepMind・NVIDIA が共同で立ち上げ、Linux Foundation 傘下のオープンソース（Apache-2.0）プロジェクトとして運営されている。剛体・関節体・布・ソフトボディ・粒子（MPM）など多様な物理現象を、8 種以上のソルバから目的に合わせて選んでシミュレーションできる。

## 既存ツールと比べて何が嬉しい？

| 観点 | Newton | MuJoCo | PyBullet | Isaac Gym |
|---|---|---|---|---|
| **GPU 演算** | ◎ Warp ネイティブ | ○ MuJoCo Warp 経由 | × CPU のみ | ◎ |
| **微分可能性** | ◎ `wp.Tape` で自動微分 | × | × | △ |
| **ソルバ選択** | ◎ 8 種（XPBD, VBD, Featherstone, MPM 等） | 1 種 | 1 種 | 1 種 |
| **布・ソフトボディ** | ◎ 専用ソルバ複数 | △ | △ | △ |
| **OpenUSD 対応** | ◎ | △ | × | △ |
| **拡張性** | ◎ Warp カーネルで自由に追加 | △ | △ | △ |
| **ガバナンス** | Linux Foundation | DeepMind 単独 | コミュニティ | NVIDIA 独自 |

**要約すると：**

- **MuJoCo** はロボ分野で最も成熟しているが、GPU ネイティブではなく微分不可。Newton は MuJoCo Warp をソルバの一つとして内蔵しつつ、それ以上のことができる。
- **PyBullet** は CPU 専用で大規模並列に不向き。
- **Isaac Gym** は GPU 高速だがプロプライエタリでソルバが固定。Newton はオープンかつソルバ選択の自由度が高い。

最大の差別化ポイントは「**問題に応じてソルバを選べる GPU ネイティブ＋微分可能な統合フレームワーク**」であること。

## 使うときの流れ

```
① インストール → ② モデル構築 → ③ ソルバ選択 → ④ シミュレーションループ → ⑤ 可視化/解析
```

### ① インストール

```bash
pip install "newton[examples]"
```

### ② ModelBuilder でシーンを組み立てる

```python
import newton

builder = newton.ModelBuilder()

# リンク（剛体）を追加し、形状を与える
link_0 = builder.add_link()
builder.add_shape_box(link_0, hx=1.0, hy=0.1, hz=0.1)

# ジョイントで接続→アーティキュレーション化
j0 = builder.add_joint_revolute(parent=-1, child=link_0, axis=(0, 0, 1))
builder.add_articulation([j0], label="arm")

# 地面を追加
builder.add_ground_plane()

# モデル確定
model = builder.finalize()
```

URDF / MJCF / USD ファイルからのインポートにも対応。

### ③ 目的に合ったソルバを選ぶ

```python
solver = newton.solvers.SolverXPBD(model)      # 剛体＋接触向け
# solver = newton.solvers.SolverFeatherstone(model)  # 関節ロボット向け
# solver = newton.solvers.SolverVBD(model)           # 布・ソフトボディ向け
# solver = newton.solvers.SolverMuJoCo(model)        # MuJoCo 互換
```

### ④ シミュレーションループを回す

```python
state_0, state_1 = model.state(), model.state()
control  = model.control()
contacts = model.contacts()

newton.eval_fk(model, model.joint_q, model.joint_qd, state_0)

for _ in range(num_steps):
    state_0.clear_forces()
    model.collide(state_0, contacts)
    solver.step(state_0, state_1, control, contacts, dt)
    state_0, state_1 = state_1, state_0   # ダブルバッファ
```

微分可能シミュレーションにしたい場合は、このループを `wp.Tape()` で囲んで `.backward()` を呼ぶだけ。

### ⑤ 可視化・解析

```bash
python -m newton.examples basic_pendulum   # ビューア付きで実行
```

`newton.viewer` による OpenGL リアルタイム描画や、OpenUSD へのエクスポートで外部ツール連携も可能。

---

**一言でまとめると：** Newton は「GPU 高速・微分可能・マルチソルバ」という三拍子を揃えたオープンな物理エンジンで、大規模ロボットシミュレーションや学習ベース制御の研究基盤として設計されている。
