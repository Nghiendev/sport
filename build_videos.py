"""Search YouTube and attach one tutorial video per BJJ skill."""
import json
import subprocess
import time
import urllib.parse
from pathlib import Path

CACHE = Path(__file__).parent / "video_cache.json"
OUT = Path(__file__).parent / "TAT-CA-KY-NANG-BJJ.md"

SKILLS: dict[str, str] = {
    "shrimp": "bjj shrimp hip escape tutorial",
    "reverse_shrimp": "bjj reverse shrimp tutorial",
    "bridge": "bjj bridge tutorial",
    "forward_roll": "bjj forward roll tutorial",
    "backward_roll": "bjj backward roll tutorial",
    "technical_standup": "bjj technical stand up tutorial",
    "crab_walk": "bjj crab walk drill",
    "penetration_step": "bjj penetration step wrestling",
    "level_change": "bjj level change wrestling",
    "granby_roll": "bjj granby roll tutorial",
    "collar_tie": "bjj collar tie tutorial",
    "inside_tie": "bjj inside tie wrestling",
    "wrist_control": "bjj wrist control standing",
    "arm_drag": "bjj arm drag tutorial",
    "snapdown": "bjj snapdown wrestling",
    "underhook": "bjj underhook tutorial",
    "overhook": "bjj whizzer overhook tutorial",
    "russian_tie": "bjj russian tie wrestling",
    "pummeling": "bjj pummeling underhook",
    "head_positioning": "bjj head position clinch",
    "hip_throw": "bjj o goshi hip throw tutorial",
    "foot_sweep": "de ashi barai bjj tutorial",
    "knee_wheel": "hiza guruma tutorial",
    "shoulder_throw": "seoi nage bjj tutorial",
    "leg_reap": "ko soto gari tutorial",
    "ankle_pick_judo": "ankle pick takedown bjj",
    "drop_seoi": "drop seoi nage tutorial",
    "double_leg": "bjj double leg takedown tutorial",
    "single_leg": "bjj single leg takedown tutorial",
    "high_crotch": "high crotch takedown bjj",
    "duck_under": "duck under takedown bjj",
    "arm_drag_takedown": "arm drag takedown bjj",
    "body_lock_takedown": "body lock takedown bjj",
    "ankle_pick": "ankle pick bjj tutorial",
    "knee_tap": "knee tap takedown wrestling",
    "sprawl": "bjj sprawl defense tutorial",
    "guard_pull": "bjj guard pull tutorial",
    "whizzer_sprawl": "whizzer sprawl bjj",
    "break_fall": "bjj breakfall ukemi",
    "posture_clinch": "bjj clinch posture",
    "closed_guard_bottom": "bjj closed guard fundamentals",
    "closed_guard_top": "bjj closed guard posture pass",
    "collar_sleeve_guard": "collar sleeve guard bjj",
    "spider_guard": "spider guard bjj tutorial",
    "lasso_guard": "lasso guard bjj tutorial",
    "butterfly_guard": "butterfly guard bjj tutorial",
    "de_la_riva": "de la riva guard tutorial",
    "reverse_dlr": "reverse de la riva guard",
    "x_guard": "x guard bjj tutorial",
    "single_leg_x": "single leg x guard tutorial",
    "shin_on_shin": "shin on shin guard bjj",
    "fifty_fifty": "50 50 guard bjj",
    "inverted_guard": "inverted guard bjj",
    "k_guard": "k guard bjj leg entanglements",
    "z_guard": "z guard knee shield bjj",
    "standard_half": "half guard fundamentals bjj",
    "deep_half": "deep half guard tutorial",
    "half_butterfly": "half butterfly guard bjj",
    "lockdown": "lockdown half guard 10th planet",
    "knee_shield_half": "knee shield half guard",
    "side_control": "side control bjj tutorial",
    "knee_on_belly": "knee on belly bjj tutorial",
    "mount": "mount position bjj tutorial",
    "rear_mount": "back control hooks bjj",
    "turtle": "turtle position bjj",
    "rnc": "rear naked choke tutorial bjj",
    "guillotine": "guillotine choke bjj tutorial",
    "triangle": "triangle choke bjj tutorial",
    "cross_collar": "cross collar choke bjj",
    "bow_arrow": "bow and arrow choke bjj",
    "ezekiel": "ezekiel choke bjj",
    "arm_triangle": "arm triangle choke bjj",
    "darce": "darce choke bjj tutorial",
    "anaconda": "anaconda choke bjj tutorial",
    "north_south_choke": "north south choke bjj",
    "clock_choke": "clock choke bjj turtle",
    "baseball_bat_choke": "baseball bat choke bjj",
    "loop_choke": "loop choke bjj",
    "peruvian_necktie": "peruvian necktie bjj",
    "gogoplata": "gogoplata bjj tutorial",
    "inverted_triangle": "inverted triangle choke bjj",
    "armbar": "armbar from guard bjj tutorial",
    "kimura": "kimura lock bjj tutorial",
    "americana": "americana lock bjj tutorial",
    "omoplata": "omoplata bjj tutorial",
    "straight_armlock": "straight armlock bjj",
    "wristlock": "wrist lock bjj tutorial",
    "ankle_lock": "straight ankle lock bjj",
    "heel_hook": "heel hook bjj john danaher",
    "kneebar": "kneebar bjj tutorial",
    "toe_hold": "toe hold bjj tutorial",
    "calf_slicer": "calf slicer bjj",
    "estima_lock": "estima lock bjj",
    "aoki_lock": "aoki lock bjj",
    "hip_bump_sweep": "hip bump sweep bjj",
    "scissor_sweep": "scissor sweep bjj tutorial",
    "flower_sweep": "flower sweep pendulum bjj",
    "lumberjack_sweep": "lumberjack sweep bjj",
    "balloon_sweep": "balloon sweep bjj",
    "waiter_sweep": "waiter sweep bjj",
    "omoplata_sweep": "omoplata sweep bjj",
    "tripod_sweep": "tripod sweep bjj",
    "butterfly_sweep": "butterfly sweep bjj tutorial",
    "hook_sweep": "hook sweep butterfly guard",
    "dlr_sweep": "de la riva sweep bjj",
    "berimbolo": "berimbolo bjj tutorial",
    "spider_sweep": "spider guard sweep bjj",
    "lasso_sweep": "lasso guard sweep",
    "x_guard_sweep": "x guard sweep bjj",
    "slx_sweep": "single leg x sweep",
    "shin_sweep": "shin on shin sweep bjj",
    "old_school_sweep": "old school sweep half guard",
    "tomahawk_sweep": "tomahawk sweep bjj",
    "foot_grab_sweep": "foot grab sweep bjj",
    "john_wayne_sweep": "john wayne sweep bjj",
    "backroll_sweep": "backroll sweep half guard",
    "coyote_sweep": "coyote sweep half guard",
    "electric_chair": "electric chair sweep bjj",
    "sumi_gaeshi": "sumi gaeshi turtle bjj",
    "rolling_sweep": "rolling sweep bjj turtle",
    "firemans_carry": "fireman carry takedown bjj",
    "same_side_knee_slide": "same side knee slice pass bjj",
    "cross_knee_slide": "cross knee slide pass bjj",
    "standing_pass": "standing guard pass bjj",
    "stack_pass": "stack pass bjj",
    "over_under_pass": "over under guard pass bjj",
    "double_under_pass": "double under pass bjj",
    "leg_drag": "leg drag pass bjj tutorial",
    "toreando": "toreando pass bullfighter bjj",
    "knee_slice": "knee slice pass bjj tutorial",
    "leg_weave": "leg weave pass bjj",
    "x_pass": "x pass bjj guard",
    "long_step": "long step pass bjj",
    "float_pass": "float pass bjj",
    "smash_pass": "smash pass butterfly guard",
    "knee_slide_mount": "knee slide to mount half guard",
    "backstep_pass": "backstep pass half guard",
    "crossface_underhook": "crossface underhook pass",
    "leg_weave_half": "leg weave half guard pass",
    "upa": "upa bridge roll mount escape bjj",
    "elbow_knee_escape": "elbow knee escape mount bjj",
    "heel_drag_escape": "heel drag escape mount",
    "gift_wrap_escape": "gift wrap escape bjj",
    "hip_escape_side": "hip escape side control bjj",
    "bridge_escape_side": "bridge escape side control",
    "elbow_push_shrimp": "elbow escape side control bjj",
    "turn_turtle_escape": "turn to turtle side control escape",
    "underhook_escape_side": "underhook escape side control",
    "back_escape": "escape rear mount bjj",
    "running_man_escape": "running man escape knee on belly",
    "foot_trap_escape": "foot trap escape knee on belly",
    "bridge_kob": "bridge escape knee on belly",
    "granby_escape": "granby roll turtle escape",
    "sitout": "sit out turtle escape wrestling",
    "stand_turtle": "stand up in turtle bjj",
    "peek_out": "peek out turtle bjj",
    "headlock_escape": "headlock escape standing bjj self defense",
    "bear_hug_escape": "bear hug escape bjj",
    "mounted_headlock": "mounted headlock escape",
    "seatbelt_hooks": "seatbelt back control hooks bjj",
    "arm_drag_back": "arm drag to back bjj",
    "kimura_back": "kimura back take bjj",
    "crab_ride": "crab ride bjj tutorial",
    "truck": "truck position bjj",
    "roll_armbar_back": "rolling armbar back take",
    "gift_wrap_back": "gift wrap back take bjj",
    "knee_cut_back": "knee cut back take half guard",
    "pressure_pin": "pressure side control bjj",
    "crossface": "crossface side control bjj",
    "hip_block": "hip block side control",
    "knee_drive": "knee drive side to mount",
    "hook_maintenance": "maintain back hooks bjj",
    "body_triangle": "body triangle back control",
    "gift_wrap_pin": "gift wrap side control",
    "crucifix": "crucifix position bjj",
    "collar_tie_top": "collar tie top control bjj",
    "scoop_grip": "scoop grip underhook bjj",
    "punch_defence": "bjj standing punch defense",
    "knee_pressure_takedown": "knee pressure takedown bear hug",
    "ground_strikes_defence": "bjj self defense ground punches",
    "guard_retention": "guard retention bjj",
    "scrambling": "bjj scrambling tutorial",
    "grip_fighting": "bjj grip fighting gi",
    "frame_escape": "framing escape bjj",
    "chain_attacks": "submission chains bjj",
    "counter_submission": "counter submissions bjj",
    "rolling_focus": "bjj rolling tips beginners",
    "pacing": "bjj pacing rolling",
    "good_partner": "bjj training partner etiquette",
    "positional_sparring": "positional sparring bjj",
    "ego_management": "bjj ego tap learn",
    "breathing": "bjj breathing claustrophobia",
}

OVERRIDES: dict[str, tuple[str, str]] = {
    "shrimp": ("x0c__MAS0DU", "Grappling Drills - Shrimp"),
    "rnc": ("176SLdBhj_A", "Rear Naked Choke - Stephan Kesting"),
    "guillotine": ("RfwI9V7gKwQ", "Guillotine - Stephan Kesting"),
    "triangle": ("5UrATWw9ajQ", "Triangle Choke - Stephan Kesting"),
    "armbar": ("pQ43Oy5k9yQ", "Armbar From Guard - John Danaher"),
}

ROW_MAP: list[tuple[str, str]] = [
    ("| Tôm / Shrimp |", "shrimp"),
    ("| Tôm ngược |", "reverse_shrimp"),
    ("| Cầu |", "bridge"),
    ("| Lăn trước |", "forward_roll"),
    ("| Lăn sau |", "backward_roll"),
    ("| Đứng kỹ thuật |", "technical_standup"),
    ("| Bò cua |", "crab_walk"),
    ("| Penetration step |", "penetration_step"),
    ("| Level change |", "level_change"),
    ("| Granby roll |", "granby_roll"),
    ("| Collar tie |", "collar_tie"),
    ("| Inside tie |", "inside_tie"),
    ("| Wrist control |", "wrist_control"),
    ("| Arm drag |", "arm_drag"),
    ("| Snapdown |", "snapdown"),
    ("| Underhook |", "underhook"),
    ("| Overhook / Whizzer |", "overhook"),
    ("| Russian tie (2-on-1) |", "russian_tie"),
    ("| Pummeling |", "pummeling"),
    ("| Head positioning |", "head_positioning"),
    ("| Hip throw |", "hip_throw"),
    ("| Foot sweep |", "foot_sweep"),
    ("| Knee wheel |", "knee_wheel"),
    ("| Shoulder throw |", "shoulder_throw"),
    ("| Leg reap |", "leg_reap"),
    ("| Ankle pick | — | ⭐ |", "ankle_pick_judo"),
    ("| Drop seoi |", "drop_seoi"),
    ("| Double leg |", "double_leg"),
    ("| Single leg |", "single_leg"),
    ("| High crotch |", "high_crotch"),
    ("| Duck under |", "duck_under"),
    ("| Arm drag takedown |", "arm_drag_takedown"),
    ("| Body lock takedown |", "body_lock_takedown"),
    ("| Ankle pick | Gạt", "ankle_pick"),
    ("| Knee tap |", "knee_tap"),
    ("| Sprawl | Chống", "sprawl"),
    ("| Guard pull |", "guard_pull"),
    ("| Whizzer + sprawl |", "whizzer_sprawl"),
    ("| Break fall (Ukemi) |", "break_fall"),
    ("| Posture in clinch |", "posture_clinch"),
    ("| Bottom | Khóa chân", "closed_guard_bottom"),
    ("| Top | Posture", "closed_guard_top"),
    ("| **Collar-Sleeve** |", "collar_sleeve_guard"),
    ("| **Spider Guard** |", "spider_guard"),
    ("| **Lasso Guard** |", "lasso_guard"),
    ("| **Butterfly Guard** |", "butterfly_guard"),
    ("| **De La Riva (DLR)** |", "de_la_riva"),
    ("| **Reverse DLR** |", "reverse_dlr"),
    ("| **X-Guard** |", "x_guard"),
    ("| **Single Leg X** |", "single_leg_x"),
    ("| **Shin-on-Shin** |", "shin_on_shin"),
    ("| **50/50 Guard** |", "fifty_fifty"),
    ("| **Inverted Guard** |", "inverted_guard"),
    ("| **K-Guard** |", "k_guard"),
    ("| **Z-Guard** |", "z_guard"),
    ("| Standard half |", "standard_half"),
    ("| Deep half |", "deep_half"),
    ("| Half butterfly |", "half_butterfly"),
    ("| Lockdown |", "lockdown"),
    ("| Knee shield half |", "knee_shield_half"),
    ("| Kiểm soát bên |", "side_control"),
    ("| Gối đè bụng |", "knee_on_belly"),
    ("| Cưỡi ngựa |", "mount"),
    ("| Lấy lưng |", "rear_mount"),
    ("| Rùa |", "turtle"),
    ("| **Rear Naked Choke (RNC)** |", "rnc"),
    ("| **Guillotine** |", "guillotine"),
    ("| **Triangle choke** |", "triangle"),
    ("| **Cross collar choke** |", "cross_collar"),
    ("| **Bow and arrow** |", "bow_arrow"),
    ("| **Ezekiel choke** |", "ezekiel"),
    ("| **Arm triangle (Head & arm)** |", "arm_triangle"),
    ("| **D'Arce choke** |", "darce"),
    ("| **Anaconda choke** |", "anaconda"),
    ("| **North-South choke** |", "north_south_choke"),
    ("| **Clock choke** |", "clock_choke"),
    ("| **Baseball bat choke** |", "baseball_bat_choke"),
    ("| **Loop choke** |", "loop_choke"),
    ("| **Peruvian necktie** |", "peruvian_necktie"),
    ("| **Gogoplata** |", "gogoplata"),
    ("| **Inverted triangle** |", "inverted_triangle"),
    ("| **Armbar (Juji gatame)** |", "armbar"),
    ("| **Kimura** | Khóa", "kimura"),
    ("| **Americana (Keylock/V-lock)** |", "americana"),
    ("| **Omoplata** |", "omoplata"),
    ("| **Straight armlock** |", "straight_armlock"),
    ("| **Wristlock** |", "wristlock"),
    ("| **Straight ankle lock (Botinha)** |", "ankle_lock"),
    ("| **Heel hook (inside/outside)** |", "heel_hook"),
    ("| **Kneebar** |", "kneebar"),
    ("| **Toe hold** |", "toe_hold"),
    ("| **Calf slicer** |", "calf_slicer"),
    ("| **Estima lock** |", "estima_lock"),
    ("| **Aoki lock** |", "aoki_lock"),
    ("| Hip bump sweep |", "hip_bump_sweep"),
    ("| Scissor sweep |", "scissor_sweep"),
    ("| Flower / Pendulum sweep |", "flower_sweep"),
    ("| Lumberjack sweep |", "lumberjack_sweep"),
    ("| Balloon sweep |", "balloon_sweep"),
    ("| Waiter sweep |", "waiter_sweep"),
    ("| Omoplata sweep |", "omoplata_sweep"),
    ("| Tripod sweep |", "tripod_sweep"),
    ("| Butterfly sweep |", "butterfly_sweep"),
    ("| Hook sweep |", "hook_sweep"),
    ("| De La Riva sweep |", "dlr_sweep"),
    ("| Berimbolo |", "berimbolo"),
    ("| Spider sweep |", "spider_sweep"),
    ("| Lasso sweep |", "lasso_sweep"),
    ("| X-Guard sweep |", "x_guard_sweep"),
    ("| Single leg X sweep |", "slx_sweep"),
    ("| Shin-on-shin sweep |", "shin_sweep"),
    ("| Old school sweep |", "old_school_sweep"),
    ("| Tomahawk sweep |", "tomahawk_sweep"),
    ("| Foot grab sweep |", "foot_grab_sweep"),
    ("| Old school (underhook) |", "old_school_sweep"),
    ("| John Wayne sweep |", "john_wayne_sweep"),
    ("| Backroll sweep |", "backroll_sweep"),
    ("| Coyote sweep |", "coyote_sweep"),
    ("| Electric chair sweep |", "electric_chair"),
    ("| Sumi gaeshi |", "sumi_gaeshi"),
    ("| Rolling sweep |", "rolling_sweep"),
    ("| Fireman's carry |", "firemans_carry"),
    ("| Same-side knee slide |", "same_side_knee_slide"),
    ("| Cross knee slide |", "cross_knee_slide"),
    ("| Standing pass |", "standing_pass"),
    ("| Stack pass |", "stack_pass"),
    ("| Over-under pass |", "over_under_pass"),
    ("| Double under / Double stack |", "double_under_pass"),
    ("| Leg drag | Kéo", "leg_drag"),
    ("| Toreando (Bullfighter) |", "toreando"),
    ("| Knee slice (Knee cut) |", "knee_slice"),
    ("| Leg weave |", "leg_weave"),
    ("| X-pass |", "x_pass"),
    ("| Long step pass |", "long_step"),
    ("| Float pass |", "float_pass"),
    ("| Smash pass |", "smash_pass"),
    ("| Knee slide to mount |", "knee_slide_mount"),
    ("| Backstep pass |", "backstep_pass"),
    ("| Crossface + underhook |", "crossface_underhook"),
    ("| Leg weave half |", "leg_weave_half"),
    ("| Upa / Bridge and roll |", "upa"),
    ("| Elbow-knee escape |", "elbow_knee_escape"),
    ("| Heel drag |", "heel_drag_escape"),
    ("| Gift wrap escape |", "gift_wrap_escape"),
    ("| Hip escape to guard |", "hip_escape_side"),
    ("| Bridge escape |", "bridge_escape_side"),
    ("| Elbow push + shrimp |", "elbow_push_shrimp"),
    ("| Turn to knees (turtle) |", "turn_turtle_escape"),
    ("| Underhook escape |", "underhook_escape_side"),
    ("| Running man |", "running_man_escape"),
    ("| Foot trap |", "foot_trap_escape"),
    ("| Bridge + roll |", "bridge_kob"),
    ("| Granby roll | Lăn", "granby_escape"),
    ("| Sit-out |", "sitout"),
    ("| Stand up in turtle |", "stand_turtle"),
    ("| Peek out |", "peek_out"),
    ("| Headlock standing |", "headlock_escape"),
    ("| Bear hug từ sau |", "bear_hug_escape"),
    ("| Mounted headlock |", "mounted_headlock"),
    ("| Seatbelt + hooks |", "seatbelt_hooks"),
    ("| Arm drag → back |", "arm_drag_back"),
    ("| Kimura trap → back |", "kimura_back"),
    ("| Crab ride |", "crab_ride"),
    ("| Truck |", "truck"),
    ("| Roll through armbar → back |", "roll_armbar_back"),
    ("| Gift wrap pass → back |", "gift_wrap_back"),
    ("| Knee cut → back take |", "knee_cut_back"),
    ("| Pressure / dead weight |", "pressure_pin"),
    ("| Crossface |", "crossface"),
    ("| Hip block |", "hip_block"),
    ("| Knee drive |", "knee_drive"),
    ("| Hook maintenance |", "hook_maintenance"),
    ("| Body triangle |", "body_triangle"),
    ("| Gift wrap | Side", "gift_wrap_pin"),
    ("| Crucifix |", "crucifix"),
    ("| Collar tie from top |", "collar_tie_top"),
    ("| Scoop grip |", "scoop_grip"),
    ("| Đứng bị khóa đầu |", "headlock_escape"),
    ("| Đứng bị đấm |", "punch_defence"),
    ("| Bị ôm từ sau |", "knee_pressure_takedown"),
    ("| Trên đất bị đấm |", "ground_strikes_defence"),
    ("| Guard retention |", "guard_retention"),
    ("| Scrambling |", "scrambling"),
    ("| Grip fighting |", "grip_fighting"),
    ("| Frame & escape |", "frame_escape"),
    ("| Chain attacks |", "chain_attacks"),
    ("| Counter submission |", "counter_submission"),
    ("| **Tập trung khi rolling** |", "rolling_focus"),
    ("| **Pacing** |", "pacing"),
    ("| **Là đối tác tốt** |", "good_partner"),
    ("| **Positional sparring** |", "positional_sparring"),
    ("| **Ego management** |", "ego_management"),
    ("| **Breathing** |", "breathing"),
    ("- [ ] Shrimp / hip escape", "shrimp"),
    ("- [ ] Bridge", "bridge"),
    ("- [ ] Technical stand-up", "technical_standup"),
    ("- [ ] Forward roll", "forward_roll"),
    ("- [ ] Backward roll", "backward_roll"),
    ("- [ ] Granby roll", "granby_roll"),
    ("- [ ] Penetration step", "penetration_step"),
    ("- [ ] Sprawl", "sprawl"),
    ("- [ ] Break fall", "break_fall"),
    ("- [ ] Level change", "level_change"),
    ("- [ ] Double leg", "double_leg"),
    ("- [ ] Single leg", "single_leg"),
    ("- [ ] Hip throw (basic)", "hip_throw"),
    ("- [ ] Arm drag", "arm_drag"),
    ("- [ ] Guard pull", "guard_pull"),
    ("- [ ] Closed guard control", "closed_guard_bottom"),
    ("- [ ] Break posture", "closed_guard_top"),
    ("- [ ] Armbar from guard", "armbar"),
    ("- [ ] Triangle", "triangle"),
    ("- [ ] Kimura from guard", "kimura"),
    ("- [ ] Guillotine", "guillotine"),
    ("- [ ] Hip bump sweep", "hip_bump_sweep"),
    ("- [ ] Scissor sweep", "scissor_sweep"),
    ("- [ ] Flower sweep", "flower_sweep"),
    ("- [ ] Posture in closed guard", "closed_guard_top"),
    ("- [ ] Open closed guard", "standing_pass"),
    ("- [ ] Knee slice pass", "knee_slice"),
    ("- [ ] Toreando pass", "toreando"),
    ("- [ ] Over-under pass", "over_under_pass"),
    ("- [ ] Side control hold", "side_control"),
    ("- [ ] Side → mount", "knee_drive"),
    ("- [ ] Side → knee on belly", "knee_on_belly"),
    ("- [ ] Knee on belly hold", "knee_on_belly"),
    ("- [ ] Mount hold", "mount"),
    ("- [ ] Americana", "americana"),
    ("- [ ] Armbar from mount", "armbar"),
    ("- [ ] Take the back from mount", "roll_armbar_back"),
    ("- [ ] Seatbelt + hooks", "seatbelt_hooks"),
    ("- [ ] Rear naked choke", "rnc"),
    ("- [ ] Maintain back control", "hook_maintenance"),
    ("- [ ] Armbar from back", "armbar"),
    ("- [ ] Upa from mount", "upa"),
    ("- [ ] Elbow-knee from mount", "elbow_knee_escape"),
    ("- [ ] Hip escape from side", "hip_escape_side"),
    ("- [ ] Bridge escape from side", "bridge_escape_side"),
    ("- [ ] Turtle escape from side", "turn_turtle_escape"),
    ("- [ ] Back escape (hand fight)", "back_escape"),
    ("- [ ] Knee on belly escape", "running_man_escape"),
    ("- [ ] Half guard recovery", "standard_half"),
]

HEADER_FIX = {
    "| Kỹ năng | Tiếng Anh | Mô tả | Mức |": "| Kỹ năng | Tiếng Anh | Mô tả | Mức | 📺 Video |",
    "| Kỹ thuật | Tiếng Nhật / EN | Mức |": "| Kỹ thuật | Tiếng Nhật / EN | Mức | 📺 Video |",
    "| Kỹ thuật | Mô tả | Mức |": "| Kỹ thuật | Mô tả | Mức | 📺 Video |",
    "| Kỹ thuật | Từ vị trí | Mức |": "| Kỹ thuật | Từ vị trí | Mức | 📺 Video |",
    "| Kỹ thuật | Cơ chế | Từ vị trí | Mức |": "| Kỹ thuật | Cơ chế | Từ vị trí | Mức | 📺 Video |",
    "| Kỹ thuật | Mức | Ghi chú |": "| Kỹ thuật | Mức | Ghi chú | 📺 Video |",
    "| Kỹ thuật | Guard | Mức |": "| Kỹ thuật | Guard | Mức | 📺 Video |",
    "| Kỹ thuật | Tiếng Anh | Mức |": "| Kỹ thuật | Tiếng Anh | Mức | 📺 Video |",
    "| Kỹ thuật | Chống guard | Mức |": "| Kỹ thuật | Chống guard | Mức | 📺 Video |",
    "| Kỹ năng | Áp dụng |": "| Kỹ năng | Áp dụng | 📺 Video |",
    "| Kỹ năng | Mô tả |": "| Kỹ năng | Mô tả | 📺 Video |",
    "| Guard | Đặc điểm | Sweep / Sub chính |": "| Guard | Đặc điểm | Sweep / Sub chính | 📺 Video |",
    "| Biến thể | Mô tả |": "| Biến thể | Mô tả | 📺 Video |",
    "| Vị trí | Tiếng Anh | Biến thể |": "| Vị trí | Tiếng Anh | Biến thể | 📺 Video |",
    "| Tình huống | Kỹ thuật |": "| Tình huống | Kỹ thuật | 📺 Video |",
    "| Bước | Hành động |": "| Bước | Hành động | 📺 Video |",
    "| Khía cạnh | Kỹ năng |": "| Khía cạnh | Kỹ năng | 📺 Video |",
}


def search_youtube(query: str) -> tuple[str, str]:
    queries = [query, query.replace("bjj ", ""), f"{query} grappling"]
    last_err = ""
    for q in queries:
        cmd = [
            "python", "-m", "yt_dlp",
            f"ytsearch3:{q}",
            "--print", "%(id)s|%(title)s",
            "--no-download",
            "--quiet",
            "--ignore-errors",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        for line in (result.stdout or "").strip().splitlines():
            if "|" in line and len(line.split("|", 1)[0].strip()) == 11:
                vid, title = line.split("|", 1)
                return vid.strip(), title.strip()
        last_err = result.stderr or result.stdout
        time.sleep(0.5)
    raise RuntimeError(f"No result for: {query}\n{last_err}")


def load_cache() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def get_video(key: str, cache: dict) -> tuple[str, str]:
    if key in cache:
        return cache[key]["id"], cache[key]["title"]
    if key in OVERRIDES:
        vid, title = OVERRIDES[key]
    else:
        print(f"  [{len(cache)+1}] {SKILLS[key]}")
        try:
            vid, title = search_youtube(SKILLS[key])
        except RuntimeError as e:
            print(f"    WARN: {e}")
            q = urllib.parse.quote(SKILLS[key])
            cache[key] = {"id": None, "title": SKILLS[key], "search": f"https://www.youtube.com/results?search_query={q}"}
            save_cache(cache)
            return "", SKILLS[key]
        time.sleep(0.8)
    cache[key] = {"id": vid, "title": title}
    save_cache(cache)
    return vid, title


def link(vid: str, title: str, search_url: str | None = None) -> str:
    short = (title[:42] + "…") if len(title) > 42 else title
    if not vid and search_url:
        return f"[📺 Tìm: {short}]({search_url})"
    return f"[📺 {short}](https://www.youtube.com/watch?v={vid})"


def append_video_cell(line: str, vid_link: str) -> str:
    if vid_link in line:
        return line
    s = line.rstrip()
    if s.endswith("|"):
        return s[:-1].rstrip() + f" {vid_link} |\n"
    return line.rstrip() + f" — {vid_link}\n"


def process_md(text: str, cache: dict) -> str:
    keys_needed = {k for _, k in ROW_MAP}
    print(f"Fetching {len(keys_needed)} videos...")
    for key in sorted(keys_needed):
        if key not in cache:
            get_video(key, cache)

    key_to_link = {
        k: link(
            cache[k].get("id") or "",
            cache[k]["title"],
            cache[k].get("search"),
        )
        for k in cache
        if k in keys_needed
    }

    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped in HEADER_FIX:
            out.append(HEADER_FIX[stripped] + "\n")
            i += 1
            if i < len(lines) and lines[i].strip().startswith("|---"):
                out.append(lines[i].rstrip() + "|---|\n")
                i += 1
            continue

        if stripped == "| Kỹ năng | Tiếng Anh | Mô tả | Mức |":
            out.append("| Kỹ năng | Tiếng Anh | Mô tả | Mức | 📺 Video |\n")
            i += 1
            if i < len(lines) and lines[i].strip().startswith("|---"):
                out.append("|---------|-----------|-------|-----|----------|\n")
                i += 1
            continue

        for frag, key in ROW_MAP:
            if frag in line and key in key_to_link:
                line = append_video_cell(line, key_to_link[key])
                break

        if stripped.startswith("| 1 | Hand fight") or stripped.startswith("| 2 | Clear hooks") or stripped.startswith("| 3 | Turn in") or stripped.startswith("| 4 | Scoot hips"):
            if "back_escape" in key_to_link:
                line = append_video_cell(line, key_to_link["back_escape"])

        out.append(line)
        i += 1

    result = "".join(out)
    note = "- Mỗi kỹ năng có link **📺 YouTube** (1 video tutorial)"
    if note not in result:
        result = result.replace(
            "- Ký hiệu mức độ: ⭐ Sơ cấp | ⭐⭐ Trung cấp | ⭐⭐⭐ Nâng cao",
            f"- Ký hiệu mức độ: ⭐ Sơ cấp | ⭐⭐ Trung cấp | ⭐⭐⭐ Nâng cao\n{note}",
        )
    # Remove old generic youtube block under section 3
    result = result.replace(
        "\n**YouTube gợi ý:**\n- [Grappling Drills — Shrimp](https://www.youtube.com/watch?v=x0c__MAS0DU) (Stephan Kesting)\n- Tìm: `BJJ solo drills beginner` — kênh: Grapplearts, Chewjitsu, Knight Jiu-Jitsu\n",
        "\n",
    )
    result = result.replace(
        "\n**YouTube gợi ý:**\n- `John Danaher standing grappling`\n- `Chewjitsu wrestling for BJJ`\n- `Lachlan Giles takedown`\n",
        "\n",
    )
    result = result.replace(
        "\n**YouTube RNC:** [Stephan Kesting RNC tutorial](https://www.youtube.com/watch?v=176SLdBhj_A)\n",
        "\n",
    )
    return result


def main():
    cache = load_cache()
    text = OUT.read_text(encoding="utf-8")
    updated = process_md(text, cache)
    OUT.write_text(updated, encoding="utf-8")
    print(f"Done. {len(cache)} videos cached -> {OUT}")


if __name__ == "__main__":
    main()
