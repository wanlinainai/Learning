/**
 * 工具函数
 */

// 时间戳格式化
export function formatDate(timestamp, part) {
  if(!timestamp) {
    return;
  }
  let date = new Date(parseInt(timestamp));

  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  let day = date.getDate();

  let hour = date.getHours();
  let minutes = date.getMinutes();
  let seconds = date.getSeconds();

  let weekArr = [
    "星期日",
    "星期一",
    "星期二",
    "星期三",
    "星期四",
    "星期五",
    "星期六"
  ]

    let week = weekArr[date.getDay()];

  // 需要给一位数前面加 0
  // 9 点 ----> 09:45:03

  if (month >= 1 && month <= 9) {
    // month += '0'; // a += b ----> a = a + b
    month = "0" + month;
  }

  if (day >= 0 && day <= 9) {
    day = "0" + day;
  }

  if (hour >= 0 && hour <= 9) {
    hour = "0" + hour;
  }

  if (minutes >= 0 && minutes <= 9) {
    minutes = "0" + minutes;
  }

  if (seconds >= 0 && seconds <= 9) {
    seconds = "0" + seconds;
  }

  let str = "";
  // 添加的part用于进行不同类型的日期展示
  switch(part) {
    case "year": {
      str = `${year}-${month}-${day}`;
      break;
    }
    case "time": {
      str = `${hour}:${minutes}:${seconds}`;
      break;
    }
    case "year-time": {
      str = `${year}-${month}-${day} ${hour}:${minutes}:${seconds}`
      break;
    }
    case "time-week": {
      str = `${hour}:${minutes}:${seconds} ${week}`;
      break;
    }
    default: {
      str = `${year}-${month}-${day} ${hour}:${minutes}:${seconds} ${week}`;
    }
  }
  return str
}