var https = require('https');
var fs = require('fs');
var path = require('path');
// 专为服务器设计的核心 jQuery
var cheerio = require('cheerio');

// 爬虫的 URL 信息
var option = {
  hostname: 'movie.douban.com',
  path: '/top250',
  port: 443
}
// 创建 http get 请求
https.get(option, function(res) {
  // 这里的 res 是 Class: http.IncomingMessage 的一个实例
  var html = '';   // 保存抓取到的 HTML 源码
  var movies = [];   // 保存解析 HTML 后的数据，即我们需要的电影信息

  // 而 http.IncomingMessage 实现了 stream.Readable 接口
  res.setEncoding('utf-8');

  // 抓取页面内容
  res.on('data', function(chunk) {
    html += chunk;
  });
  // 'end' 事件将在流中再没有数据可供消费时触发
  res.on('end', function() {
    // 使用 cheerio 加载抓取到的 HTML 代码
    let $ = cheerio.load(html);
    // 解析页面 | 迭代 cheerio 对象，为每个匹配的元素执行一个函数
    $('.item').each(function() {
      let movie = {
        title: $('.title', this).text(),   // 获取电影名称
        star: $('.star .rating_num', this).text(),   // 获取电影评分
        link: $('a', this).attr('href'),   // 获取电影详情页链接
        picUrl: $('.pic img', this).attr('src')   // 获取电影图片链接
      };
      // 把所有电影放在一个数组里面
      movies.push(movie);
      // 下载图片
      downloadImg('img/', movie.picUrl);
    });
    // 保存抓取到的电影数据
    saveData('data/data.json', movies);
  });
}).on('error', function(error) {
  console.log('获取数据出错...');
});

// 保存数据到本地
function saveData(path, movies) {
  // 异步地写入数据到文件            | JSON.stringify 参数 4, 表示缩进 4 个空格
  fs.writeFile(path, JSON.stringify(movies, null, 4), function(error) {
    if (error) {
      return console.log(error);
    }
    console.log('数据保存成功...');
  });
}

// 下载图片
function downloadImg(imgDir, url) {
  https.get(url, function(res) {
    var data = '';

    // 设置二进制编码
    res.setEncoding('binary');

    res.on('data', function(chunk) {
      data += chunk;
    });

    res.on('end', function() {
      fs.writeFile(imgDir + path.basename(url), data, 'binary', function(error) {
        if (error) {
          return console.log(error);
        }
        console.log('图片下载：', path.basename(url));
      });
    });
  }).on('error', function(error) {
    console.log('图片数据获取失败...')
  });
}
