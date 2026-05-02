import React, { useMemo, useState } from 'react';

function polarToCartesian(cx, cy, radius, angle) {
  const radians = ((angle - 90) * Math.PI) / 180;
  return {
    x: cx + radius * Math.cos(radians),
    y: cy + radius * Math.sin(radians),
  };
}

function describeSlice(cx, cy, radius, startAngle, endAngle) {
  const start = polarToCartesian(cx, cy, radius, endAngle);
  const end = polarToCartesian(cx, cy, radius, startAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? '0' : '1';

  return [
    `M ${cx} ${cy}`,
    `L ${end.x} ${end.y}`,
    `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${start.x} ${start.y}`,
    'Z',
  ].join(' ');
}

export default function DeviceCostPieChart({ data }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const { slices, total } = useMemo(() => {
    const sum = data.reduce((acc, item) => acc + item.value, 0);
    let cursor = 0;

    return {
      total: sum,
      slices: data.map((item) => {
        const angle = (item.value / sum) * 360;
        const slice = {
          ...item,
          startAngle: cursor,
          endAngle: cursor + angle,
        };
        cursor += angle;
        return slice;
      }),
    };
  }, [data]);

  const activeSlice = slices[activeIndex] ?? slices[0];

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 rounded-3xl bg-white/60 p-3">
        <svg viewBox="0 0 260 260" className="h-full w-full">
          <g>
            {slices.map((slice, index) => {
              const path = describeSlice(130, 130, 88, slice.startAngle, slice.endAngle);
              const isActive = index === activeIndex;
              return (
                <path
                  key={slice.key}
                  d={path}
                  fill={slice.color}
                  stroke="#ffffff"
                  strokeWidth="3"
                  opacity={isActive ? 1 : 0.78}
                  transform={isActive ? 'scale(1.03) translate(-4 -4)' : undefined}
                  style={{ cursor: 'pointer', transition: 'all 180ms ease' }}
                  onMouseEnter={() => setActiveIndex(index)}
                >
                  <title>{`${slice.name} - ${slice.section} | ₺${slice.value.toFixed(2)}/saat`}</title>
                </path>
              );
            })}
          </g>

          <circle cx="130" cy="130" r="52" fill="white" />
          <text x="130" y="122" textAnchor="middle" className="fill-on-surface text-[13px] font-semibold">
            {activeSlice?.name}
          </text>
          <text x="130" y="141" textAnchor="middle" className="fill-on-surface-variant text-[11px]">
            {activeSlice?.section}
          </text>
          <text x="130" y="158" textAnchor="middle" className="fill-primary text-[14px] font-bold">
            ₺{activeSlice?.value.toFixed(2)}
          </text>
        </svg>
      </div>

      <div className="mt-4 border-t border-surface-container pt-4">
        <div className="flex flex-wrap justify-center gap-3">
          {data.map((item, index) => (
            <button
              key={item.key}
              type="button"
              className="flex items-center gap-2 rounded-full bg-surface-container-low px-3 py-2 text-xs font-medium text-on-surface-variant transition-colors hover:bg-surface-container"
              onMouseEnter={() => setActiveIndex(index)}
            >
              <span className="h-3 w-3 rounded-full" style={{ backgroundColor: item.color }} />
              {item.name} - {item.section}
            </button>
          ))}
        </div>
        <p className="mt-3 text-center text-xs text-on-surface-variant">Toplam: ₺{total.toFixed(2)} / saat</p>
      </div>
    </div>
  );
}
