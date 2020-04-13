package xyz.ikin.utl;

import java.lang.reflect.Field;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * author : 动力节点
 * 2019/3/22 0022
 */
public class SqlSession {


    //将查询结果集内容转换为实体类对象集合

    public static List selectList(String sql,Class classFile){

        PreparedStatement ps = DBUtil.createStatement(sql);
        ResultSet rs = null;
        Field fieldArray[]=null;
        List list = new ArrayList();
        try {
            rs = ps.executeQuery();
            //1.获得当前对应的实体类所有的属性信息
            fieldArray = classFile.getDeclaredFields();
            //2.遍历结果集，将一行数据交给一个对应的实体类对象
            while(rs.next()){

               Object obj = classFile.newInstance();
               //3.读取数据行字段信息，【字段名】就是【属性名】
                for(int i=0;i<fieldArray.length;i++){

                    Field fieldObj = fieldArray[i];//private Integer deptNo
                    String  columnName = fieldObj.getName(); //deptNo;
                    String  value = rs.getString(columnName);
                    //4.将读取字段内容赋值给【当前实例对象】中【同名属性】
                    init(obj,value,fieldObj);
                }
                list.add(obj);

            }
        } catch (Exception e) {
            e.printStackTrace();
        }finally{
            DBUtil.close(rs);
        }

        return  list;

    }

    //负责将字段内容赋值给指定对象中属性
    public static void init(Object obj,String value,Field fieldObj)throws Exception{

        fieldObj.setAccessible(true);
        //读取属性对象的【数据类型名】
        String  typeName= fieldObj.getType().getName();//"java.lang.Integer","java.lang.String"
        //根据属性的数据类型名进行赋值
        if(value==null){
            fieldObj.set(obj, null);

        }else{
            if("java.lang.Integer".equals(typeName)){
                fieldObj.set(obj, Integer.valueOf(value));

            }else if("java.lang.Double".equals(typeName)){

                fieldObj.set(obj, Double.valueOf(value));
            }else if("java.lang.Long".equals(typeName)){
                fieldObj.set(obj, Long.valueOf(value));
            }else if("java.util.Date".equals(typeName)){
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-DD");
                Date date = sdf.parse(value);
                fieldObj.set(obj, date);
            }else{//"java.lang.String"
                fieldObj.set(obj, value);
            }

        }

    }

    //动态生成INSERT
    public  static int insert(Object obj){

             int flag = 0;//插入是否成功标识   0 失败   大于0添加成功
             String  tableName = null;
             Class  classFile = null;
             String classPath = null;  //"com.bjpowernode.model.Dept"
             int  startIndex=0;
             StringBuffer colunmStr = new StringBuffer("(");//(字段名1，字段名2)
             StringBuffer valueStr = new StringBuffer(" value(");
             StringBuffer sql = new StringBuffer(" INSERT INTO ");
             Field fieldArray[]=null;
             PreparedStatement ps = null;

        try {
            //1.获得【表名】
            classFile = obj.getClass();
            classPath = classFile.getName();
            startIndex=classPath.lastIndexOf(".");
            tableName = classPath.substring(startIndex+1);//Dept
            //2.动态生成赋值字段名称
            fieldArray = classFile.getDeclaredFields();
            for(int i=0;i<fieldArray.length;i++){
                Field fieldObj = fieldArray[i];
                fieldObj.setAccessible(true);
                Object value = fieldObj.get(obj);
                String typeName = fieldObj.getType().getName();
                if("java.lang.Integer".equals(typeName)){

                      if(value!=null && ((Integer)value)!=0){
                          if(colunmStr.length()==1 ||valueStr.length()==7){
                              colunmStr.append(fieldObj.getName());
                              valueStr.append(value);
                          }else{
                              colunmStr.append(",");
                              colunmStr.append(fieldObj.getName());
                              valueStr.append(",");
                              valueStr.append(value);
                          }
                      }
                }else if("java.lang.Double".equals(typeName)){

                    if(value!=null && ((Double)value)!=0){
                        if(colunmStr.length()==1 ||valueStr.length()==7){
                            colunmStr.append(fieldObj.getName());
                            valueStr.append(value);
                        }else{
                            colunmStr.append(",");
                            colunmStr.append(fieldObj.getName());
                            valueStr.append(",");
                            valueStr.append(value);
                        }
                    }
                }else if("java.lang.String".equals(typeName)){
                     if(value!=null&& !"".equals((String)value)){
                         if(colunmStr.length()==1 ||valueStr.length()==7){
                             colunmStr.append(fieldObj.getName());
                             valueStr.append("'");
                             valueStr.append(value);
                             valueStr.append("'");
                         }else{
                             colunmStr.append(",");
                             colunmStr.append(fieldObj.getName());
                             valueStr.append(",'");
                             valueStr.append(value);
                             valueStr.append("'");
                         }
                     }
                }
            }
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }

        colunmStr.append(")");
        valueStr.append(")");

        //拼装INSERT
        sql.append(tableName);
        sql.append(colunmStr);
        sql.append(valueStr);
        System.out.println(sql.toString());

        ps = DBUtil.createStatement(sql.toString());     //原代码中，sql语句并没有写入，这里将ps重新初始化

        try {
            flag = ps.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DBUtil.close(null);
        }
        System.out.println(flag);
        return flag;
    }


    public  static int insert(List list){

        int flag = 0;//插入是否成功标识   0 失败   大于0添加成功
        String  tableName = null;
        Class  classFile= null;
        String classPath=null;//"com.bjpowernode.model.Dept"
        int  startIndex=0;
        StringBuffer colunmStr=new StringBuffer("(");//(字段名1，字段名2)
        StringBuffer valueStr=new StringBuffer(" value(");
        StringBuffer sql = new StringBuffer(" INSERT INTO ");
        Field fieldArray[]=null;
        PreparedStatement ps = DBUtil.createStatement("");

        try {
            //1.获得【表名】
            classFile = list.get(0).getClass();
            classPath = classFile.getName();
            startIndex=classPath.lastIndexOf(".");
            tableName = classPath.substring(startIndex+1);//Dept
            //2.动态生成赋值字段名称
            fieldArray = classFile.getDeclaredFields();
            for(int j=0;j<list.size();j++){
                colunmStr=new StringBuffer("(");
                valueStr=new StringBuffer(" value(");
                sql = new StringBuffer(" INSERT INTO ");
                Object obj = list.get(j);
                for(int i=0;i<fieldArray.length;i++){
                    Field fieldObj = fieldArray[i];
                    fieldObj.setAccessible(true);
                    Object value = fieldObj.get(obj);
                    String typeName = fieldObj.getType().getName();
                    if("java.lang.Integer".equals(typeName)){

                        if(value!=null && ((Integer)value)!=0){
                            if(colunmStr.length()==1 ||valueStr.length()==7){
                                colunmStr.append(fieldObj.getName());
                                valueStr.append(value);
                            }else{
                                colunmStr.append(",");
                                colunmStr.append(fieldObj.getName());
                                valueStr.append(",");
                                valueStr.append(value);
                            }
                        }
                    }else if("java.lang.Double".equals(typeName)){

                        if(value!=null && ((Double)value)!=0){
                            if(colunmStr.length()==1 ||valueStr.length()==7){
                                colunmStr.append(fieldObj.getName());
                                valueStr.append(value);
                            }else{
                                colunmStr.append(",");
                                colunmStr.append(fieldObj.getName());
                                valueStr.append(",");
                                valueStr.append(value);
                            }
                        }
                    }else if("java.lang.String".equals(typeName)){
                        if(value!=null&& !"".equals((String)value)){
                            if(colunmStr.length()==1 ||valueStr.length()==7){
                                colunmStr.append(fieldObj.getName());
                                valueStr.append("'");
                                valueStr.append(value);
                                valueStr.append("'");
                            }else{
                                colunmStr.append(",");
                                colunmStr.append(fieldObj.getName());
                                valueStr.append(",'");
                                valueStr.append(value);
                                valueStr.append("'");
                            }
                        }
                    }
                }

                colunmStr.append(")");
                valueStr.append(")");

                //拼装INSERT
                sql.append(tableName);
                sql.append(colunmStr);
                sql.append(valueStr);
                System.out.println(sql.toString());

                ps.addBatch(sql.toString());
            }



            }catch (Exception e) {
            e.printStackTrace();
        }

        try {
            ps.executeBatch();
            flag=1;
        } catch (SQLException e) {
            e.printStackTrace();
            flag=0;
        } finally {
            DBUtil.close(null);
        }

        return flag;
    }

    public static  int delete(String sql){
        int flag =0;
        PreparedStatement ps = DBUtil.createStatement(sql);
        try {
            flag=ps.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DBUtil.close(null);
        }
        return flag;
    }

    public static int Update(String sql){
        int flag =0;
        PreparedStatement ps = DBUtil.createStatement(sql);
        try {
            flag=ps.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            DBUtil.close(null);
        }
        return flag;
    }

}
