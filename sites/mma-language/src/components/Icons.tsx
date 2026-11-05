import type { ReactElement, ReactNode } from "react";

type IconProps = { size?: number; className?: string };

function Svg({ size = 24, className, children }: IconProps & { children: ReactNode }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      {children}
    </svg>
  );
}

export function IconHome(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M3 10.5 12 3l9 7.5" />
      <path d="M5 10v10h14V10" />
    </Svg>
  );
}

export function IconBook(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5Z" />
      <path d="M4 5.5V21" />
    </Svg>
  );
}

export function IconLayers(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="m12 3 9 5-9 5-9-5 9-5Z" />
      <path d="m3 13 9 5 9-5" />
      <path d="m3 18 9 5 9-5" />
    </Svg>
  );
}

export function IconChart(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M4 19V5" />
      <path d="M4 19h16" />
      <path d="M8 16V10" />
      <path d="M12 16V7" />
      <path d="M16 16v-4" />
    </Svg>
  );
}

export function IconPlay(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="12" cy="12" r="9" />
      <path d="m10 8 7 4-7 4V8Z" fill="currentColor" stroke="none" />
    </Svg>
  );
}

export function IconDumbbell(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M6 8v8" />
      <path d="M18 8v8" />
      <path d="M6 10h12" />
      <path d="M6 14h12" />
      <path d="M4 9v6" />
      <path d="M20 9v6" />
    </Svg>
  );
}

export function IconLink(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M9 8H7a4 4 0 1 0 0 8h2" />
      <path d="M15 8h2a4 4 0 1 1 0 8h-2" />
      <path d="M8 12h8" />
    </Svg>
  );
}

export function IconInfo(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 11v5" />
      <path d="M12 8h.01" />
    </Svg>
  );
}

export function IconTarget(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="12" cy="12" r="8" />
      <circle cx="12" cy="12" r="4" />
      <circle cx="12" cy="12" r="1" fill="currentColor" stroke="none" />
    </Svg>
  );
}

export function IconStance(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="12" cy="5" r="2" />
      <path d="M12 7v5" />
      <path d="m8 22 4-10 4 10" />
      <path d="M7 14h10" />
    </Svg>
  );
}

export function IconFist(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M8 11V7a1.5 1.5 0 0 1 3 0v2" />
      <path d="M11 9V6.5a1.5 1.5 0 0 1 3 0V9" />
      <path d="M14 9V7a1.5 1.5 0 0 1 3 0v5c0 3-2 6-5 7.5C9 17 7 14 7 11V10a1.5 1.5 0 0 1 3 0v1" />
    </Svg>
  );
}

export function IconKick(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="8" cy="5" r="2" />
      <path d="M8 7v5l4 2 5-7" />
      <path d="m7 22 2-8" />
      <path d="m13 14 2 8" />
    </Svg>
  );
}

export function IconClinch(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="8" cy="6" r="2" />
      <circle cx="16" cy="6" r="2" />
      <path d="M6 20v-6l2-3h4l2 3v6" />
      <path d="M10 11h4" />
    </Svg>
  );
}

export function IconTakedown(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M5 5h8" />
      <path d="M9 5v6l8 6" />
      <path d="m14 13 4 1 1 5" />
      <circle cx="7" cy="16" r="2" />
    </Svg>
  );
}

export function IconGuard(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M12 3 4 7v5c0 4.5 3.2 7.8 8 9 4.8-1.2 8-4.5 8-9V7l-8-4Z" />
    </Svg>
  );
}

export function IconEscape(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M4 12h12" />
      <path d="m12 8 4 4-4 4" />
      <path d="M18 5v14" />
    </Svg>
  );
}

export function IconLock(p: IconProps) {
  return (
    <Svg {...p}>
      <rect x="5" y="11" width="14" height="10" rx="2" />
      <path d="M8 11V8a4 4 0 0 1 8 0v3" />
    </Svg>
  );
}

export function IconWhistle(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="8" cy="13" r="4" />
      <path d="M11.5 11.5 18 7h3v3l-5.5 3.5" />
      <path d="M8 11v4" />
    </Svg>
  );
}

export function IconMic(p: IconProps) {
  return (
    <Svg {...p}>
      <rect x="9" y="3" width="6" height="11" rx="3" />
      <path d="M5 11a7 7 0 0 0 14 0" />
      <path d="M12 18v3" />
      <path d="M8 21h8" />
    </Svg>
  );
}

export function IconScale(p: IconProps) {
  return (
    <Svg {...p}>
      <path d="M12 3v18" />
      <path d="M5 7h14" />
      <path d="m5 7-3 7h6L5 7Z" />
      <path d="m19 7-3 7h6l-3-7Z" />
    </Svg>
  );
}

export function IconSearch(p: IconProps) {
  return (
    <Svg {...p}>
      <circle cx="11" cy="11" r="6" />
      <path d="m20 20-4-4" />
    </Svg>
  );
}

const GROUP_ICONS: Record<string, (p: IconProps) => ReactElement> = {
  "Không gian giao đấu và chiến thuật": IconTarget,
  "Tư thế và bộ pháp": IconStance,
  "Đòn tay và phòng thủ đánh đứng": IconFist,
  "Đá gối và chỏ": IconKick,
  "Áp sát tranh tay và vật lồng": IconClinch,
  "Vào vật chống vật và chuyển tiếp": IconTakedown,
  "Vị trí địa chiến và hệ guard": IconGuard,
  "Thoát thế đảo thế đánh trên sàn": IconEscape,
  "Khóa siết và tín hiệu chịu thua": IconLock,
  "Huấn luyện dụng cụ và khẩu lệnh": IconDumbbell,
  "Tổ chức trận đấu luật và kết quả": IconWhistle,
  "Thống kê và ngôn ngữ tường thuật": IconMic,
  "Hạng cân và hồ sơ võ sĩ": IconScale,
};

export function GroupIcon({ group, size = 28 }: { group: string; size?: number }) {
  const Comp = GROUP_ICONS[group] ?? IconLayers;
  return <Comp size={size} />;
}
