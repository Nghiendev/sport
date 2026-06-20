# Sơ đồ chuyển vị trí & chuỗi tấn công BJJ

> Bản đồ trạng thái và các skill có thể móc nối thành chuỗi. Chi tiết từng kỹ năng: [TAT-CA-KY-NANG-BJJ.md](./TAT-CA-KY-NANG-BJJ.md) → `ky-nang/`.

---

## 1. Phân cấp vị trí (ai đang thắng?)

```mermaid
flowchart TB
  subgraph TOP["Top — kiểm soát tốt nhất → tệ nhất"]
    RM["Rear Mount"]
    M["Mount"]
    KOB["Knee on Belly"]
    SC["Side Control"]
    PG["Passing / trong Guard đối thủ"]
  end

  subgraph NEUTRAL["Trung tính (bottom)"]
    G["Guard — closed / open / half"]
  end

  subgraph BAD["Bottom bị pin — cần thoát"]
    SCb["Side / KOB / Mount / Back (bị)"]
    T["Turtle — vị trí chuyển tiếp"]
  end

  RM --> M
  M --> KOB
  KOB --> SC
  SC --> PG
  PG -.-> G
  G -.-> SCb
  SCb --> T
  T -.-> G
```

**Quy tắc vàng:** Nếu bạn ở dưới ngoài Guard → đang thua. Thoát hoặc về Guard trước khi nghĩ tới submission.

---

## 2. Chuyển trạng thái — Top tiến công

```mermaid
flowchart LR
  ST["Đứng / Clinch"]
  GT["Trong Guard đối thủ"]
  SIDE["Side Control"]
  KOB["Knee on Belly"]
  MNT["Mount"]
  BACK["Rear Mount"]

  ST -->|"Takedown / pull guard"| GT
  GT -->|"Pass guard"| SIDE
  SIDE -->|"Knee drive"| KOB
  SIDE -->|"Step over"| MNT
  KOB -->|"Step to mount"| MNT
  MNT -->|"Take the back"| BACK
  BACK -->|"RNC / bow & arrow"| FIN["Tap"]
```

### Skill móc nối (Top cổ điển)

| Bước | Vị trí | Kỹ năng | Chi tiết |
|------|--------|---------|----------|
| 1 | Trong Guard | [Knee cut](./ky-nang/knee-cut-pass.md), [Over-under](./ky-nang/over-under-pass.md), [Toreando](./ky-nang/toreando-pass.md) | Pass trước, khóa sau |
| 2 | Side Control | [Crossface pin](./ky-nang/crossface-pin.md), [Americana](./ky-nang/americana.md), [Knee drive → mount](./ky-nang/knee-drive-mount.md) | Giữ pin hoặc lên mount |
| 3 | Mount | [Armbar](./ky-nang/armbar.md), [Ezekiel](./ky-nang/ezekiel-choke.md), [Lấy lưng](./ky-nang/roll-through-armbar-back.md) | Position before submission |
| 4 | Rear Mount | [RNC](./ky-nang/rear-naked-choke.md), [Bow & arrow](./ky-nang/bow-and-arrow-choke.md) | Finish |

---

## 3. Chuyển trạng thái — Bottom phòng thủ / tấn công

```mermaid
flowchart TB
  subgraph ATTACK["Guard dưới — tấn công"]
    CG["Closed Guard"]
    CG -->|"Break posture"| SUB["Triangle / Armbar / Kimura"]
    CG -->|"Sweep"| SW["Hip bump / Scissor / Flower"]
    SW --> TOP["Lên top → tiếp chuỗi §2"]
  end

  subgraph OPEN["Open Guard"]
    OG["Butterfly / DLR / Spider"]
    OG --> BSW["Butterfly / DLR / X-guard sweep"]
    OG --> BT["Berimbolo / Crab ride / Arm drag back"]
    BT --> BACK["Rear Mount"]
  end

  subgraph ESC["Thoát từ pin xấu"]
    PIN["Side / Mount / Back (dưới)"]
    PIN -->|"Hip escape / bridge"| G2["Về Guard"]
    PIN -->|"Turn to knees"| TU["Turtle"]
    TU -->|"Granby / sit-out"| G2
  end
```

### Combo Closed Guard (A fail → B)

```mermaid
flowchart LR
  TRI["Triangle"] <-->|"Đối thủ stack/posture"| ARM["Armbar"]
  ARM <-->|"Đối thủ pull arm"| OMO["Omoplata"]
  TRI -->|"Arm in wrong place"| KIM["Kimura"]
```

| Chuỗi | Skill | Link |
|-------|-------|------|
| Posture → submit | Closed guard bottom, Triangle, Armbar | [closed-guard-bottom](./ky-nang/closed-guard-bottom.md), [triangle](./ky-nang/triangle-choke.md) |
| Sweep → top | Hip bump, Scissor, Flower | [hip-bump-sweep](./ky-nang/hip-bump-sweep.md), [scissor-sweep](./ky-nang/scissor-sweep.md) |
| Open → back | Berimbolo, Crab ride | [berimbolo](./ky-nang/berimbolo.md), [crab-ride](./ky-nang/crab-ride.md) |

---

## 4. Half Guard — tranh underhook

```mermaid
flowchart TB
  HG["Half Guard"]
  HG -->|"Bottom thắng underhook"| OS["Old school sweep / Dogfight"]
  HG -->|"Top thắng underhook"| CP["Crossface pass / Knee slice"]
  OS --> UP["Đứng / side top"]
  CP --> MNT["Mount / side pin"]
```

| Vai trò | Skill |
|---------|-------|
| Bottom | [Standard half](./ky-nang/standard-half-guard.md), [Old school sweep](./ky-nang/old-school-half-sweep.md), [Underhook](./ky-nang/underhook.md) |
| Top | [Crossface underhook pass](./ky-nang/crossface-underhook-pass.md), [Knee slice → mount](./ky-nang/knee-slide-to-mount-pass.md) |

---

## 5. Đứng → Ground

```mermaid
flowchart LR
  CL["Collar tie / Underhook"]
  CL --> TD["Double leg / Single / Body lock"]
  CL --> GP["Guard pull"]
  TD --> GR["Trong guard hoặc side"]
  GP --> CG["Closed / open guard"]
  GR --> SCR["Scramble + retention"]
```

---

## 6. Nguyên tắc móc nối

1. **Position before submission** — Cải thiện vị trí (pass, sweep, pin) trước khi khóa.
2. **Chain attacks** — Đòn A fail → phản ứng đối thủ mở đòn B (Americana fail → arm triangle; pass fail → đổi pass khác).
3. **Same position, multiple finishes** — Side: Americana / Kimura / arm triangle; Mount: armbar / Ezekiel / back take.
4. **Turtle = bước trung gian** — Không dừng lại; Granby/sit-out về guard hoặc đối thủ lấy back.

---

## 7. Canvas tương tác

Mở **BJJ — Chuyển vị trí & Chuỗi tấn công** trong Cursor Canvas để xem sơ đồ DAG có thể cuộn và chọn 6 chuỗi tấn công mẫu.

---

*Tham chiếu: [HUONG-DAN-BJJ.md](./HUONG-DAN-BJJ.md) §3–§7, [TAT-CA-KY-NANG-BJJ.md](./TAT-CA-KY-NANG-BJJ.md) §10.*
