const WEEKDAYS = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']

export function formatWeekday(n: number): string {
  return WEEKDAYS[n] ?? `周${n}`
}

export function formatPeriod(start: number, end: number): string {
  return start === end ? `第${start}节` : `第${start}-${end}节`
}

export function formatWeekRange(start: number, end: number): string {
  return start === end ? `第${start}周` : `第${start}-${end}周`
}

export function formatWeekLabel(week: number, weekStart: string, weekEnd: string): string {
  return `第${week}周 (${weekStart.slice(5)} ~ ${weekEnd.slice(5)})`
}

export function formatClassroom(building?: string, roomNumber?: string): string {
  if (!building || !roomNumber) return '-'
  return `${building}-${roomNumber}`
}
