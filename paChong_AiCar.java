import java.net.*;
import java.io.*;
import java.util.regex.*;
public class Pa_Chong_AiCar {
  public static void main(String[] args) throws MalformedURLException, IOException{
    pa_Chong("http://newcar.xcar.com.cn/price");
  }

  public static void pa_Chong(String str) throws MalformedURLException, IOException{
    StringBuilder str_builder = new StringBuilder(str);
    URL url = new URL(str_builder.toString());
    // 返回一个 URLConnection 对象，它表示到 URL 所引用的远程对象的连接
    URLConnection url_connection = url.openConnection();
    //  打开到此 URL 引用的资源的通信链接
    url_connection.connect();
     //获取网络读取输入流
    InputStream input = url_connection.getInputStream();
    // 缓冲字符流，用于读取数据（提高效率）
    BufferedReader buf_read = new BufferedReader(new InputStreamReader(input));
    // 创建文件用于保存数据
    File file = new File("F:" + File.separator + "File" + File.separator + "Pa_Chong_AiCar.doc");
    // 缓冲字符流，用于写入数据（提高效率）
    BufferedWriter buf_write = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file)));

// --------------------------------------------------------------------------------------------------
    //正则， 查找规则（品牌）
    String reg_1 = "<a\\shref=\"/price/[a-z0-9]+";
    // 正则，查找规则 (车系)
    String reg_2 = "<a\\shref=\"/\\d+";

    //将规则封装成对象
    Pattern pattern_1 = Pattern.compile(reg_1);
    Pattern pattern_2 = Pattern.compile(reg_2);

    String message = null;
    while ((message = buf_read.readLine()) != null) {

// -------------------------------------------------------------------------------------------
      // 让正则对象和要作用的字符串相关联，获取匹配对象
      Matcher matcher_1 = pattern_1.matcher(message);
      //将规则作用到字符串上，并进行符合规则的子串查找
      while (matcher_1.find()) {
        // 用于写入获取匹配后的结果
        buf_write.write("品牌:  ");
        // 截取网址字符串
        String find_1 = matcher_1.group().substring(15, matcher_1.group().length());
        // 结果写入文件
        buf_write.write(str_builder.toString() + find_1);
        //  写入一个行分隔符。（换行）
        buf_write.newLine();
        // 刷新
        buf_write.flush();
      }

//-------------------------------------------------------------------------------------------------
      // 让正则对象和要作用的字符串相关联，获取匹配对象
      Matcher matcher_2 = pattern_2.matcher(message);
      //将规则作用到字符串上，并进行符合规则的子串查找
      while (matcher_2.find()) {
        // 用于写入获取匹配后的结果
        buf_write.write("    车系:  ");
        // 截取网址字符串
        String find_2 = matcher_2.group().substring(9, matcher_2.group().length());
        // 用空字符串替换后的结果写入文件
        buf_write.write((str_builder + find_2).replace("/price", ""));
        //  写入一个行分隔符。（换行）
        buf_write.newLine();
        // 刷新
        buf_write.flush();
      }
    }
    buf_read.close();
    buf_write.close();
  }
}
