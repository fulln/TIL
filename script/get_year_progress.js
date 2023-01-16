function get_year_progress(length=20){
    const now = new Date()
    const year = now.getFullYear()
    const yearStart = new Date(year, 0)
    const yearEnd = new Date(year+1, 0)
    const progress = (now-yearStart)/(yearEnd-yearStart)
    const prefix = ''.padStart(Math.round(length*progress), '▓')
    const suffix = ''.padStart(length-Math.round(length*progress), '░')
    return '今年进度: '+prefix+suffix+' '+(progress*100).toFixed(2)+'%'
  }
  module.exports = get_year_progress;