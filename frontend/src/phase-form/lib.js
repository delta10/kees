export const objectDiff = (first, second) => {
  const result = {}

  Object.keys(first).forEach((key) => {
    if (JSON.stringify(first[key]) !== JSON.stringify(second[key])) {
      result[key] = JSON.parse(JSON.stringify(second[key]))
    }
  })

  Object.keys(second).forEach((key) => {
    if (JSON.stringify(second[key]) !== JSON.stringify(first[key])) {
      result[key] = JSON.parse(JSON.stringify(second[key]))
    }
  })

  return result
}
