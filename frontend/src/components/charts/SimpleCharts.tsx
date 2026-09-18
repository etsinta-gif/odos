type SeriesPoint = { label: string; value: number };

type ChartProps = {
  title: string;
  points: SeriesPoint[];
  compactLabels?: boolean;
};

export function BarChart({ title, points, compactLabels = false }: ChartProps) {
  const max = Math.max(...points.map((p) => p.value), 1);
  return (
    <div className="space-y-2">
      <p className="text-xs text-brand-deep/70">{title}</p>
      {points.map((point) => (
        <div key={point.label}>
          <div className={`flex justify-between whitespace-nowrap ${compactLabels ? 'text-[10px]' : 'text-xs'}`}><span>{point.label}</span><span>{point.value}</span></div>
          <div className="h-2 bg-brand-sand rounded">
            <div className="h-2 bg-brand-mint rounded" style={{ width: `${Math.max(4, (point.value / max) * 100)}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

export function LineChart({ title, points }: ChartProps) {
  const max = Math.max(...points.map((p) => p.value), 1);
  const min = Math.min(...points.map((p) => p.value), 0);
  const width = 300;
  const height = 120;
  const xStep = points.length > 1 ? width / (points.length - 1) : width;
  const y = (v: number) => height - ((v - min) / (max - min || 1)) * height;
  const path = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${i * xStep} ${y(p.value)}`).join(' ');

  return (
    <div className="space-y-2">
      <p className="text-xs text-brand-deep/70">{title}</p>
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-32 bg-white rounded border border-brand-deep/10">
        <path d={path} fill="none" stroke="#3f8f7b" strokeWidth="2" />
      </svg>
    </div>
  );
}

export function PieChart({ title, points }: ChartProps) {
  const total = points.reduce((acc, p) => acc + p.value, 0) || 1;
  const colors = ['#3f8f7b', '#203a5f', '#d18f2f', '#7b8ba3', '#8a5a44'];

  let acc = 0;
  const slices = points.map((p, idx) => {
    const start = (acc / total) * Math.PI * 2;
    acc += p.value;
    const end = (acc / total) * Math.PI * 2;
    const x1 = 50 + 45 * Math.cos(start);
    const y1 = 50 + 45 * Math.sin(start);
    const x2 = 50 + 45 * Math.cos(end);
    const y2 = 50 + 45 * Math.sin(end);
    const largeArc = end - start > Math.PI ? 1 : 0;
    return {
      d: `M 50 50 L ${x1} ${y1} A 45 45 0 ${largeArc} 1 ${x2} ${y2} Z`,
      color: colors[idx % colors.length],
      label: p.label,
      value: p.value,
    };
  });

  return (
    <div className="space-y-2">
      <p className="text-xs text-brand-deep/70">{title}</p>
      <div className="flex items-center gap-4">
        <svg viewBox="0 0 100 100" className="w-28 h-28">
          {slices.map((slice) => (
            <path key={slice.label} d={slice.d} fill={slice.color} />
          ))}
        </svg>
        <div className="space-y-1 text-xs">
          {slices.map((slice) => (
            <div key={slice.label} className="flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded" style={{ backgroundColor: slice.color }} />
              <span>{slice.label}: {slice.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
