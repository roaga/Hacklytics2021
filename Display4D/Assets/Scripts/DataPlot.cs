﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class DataPlot : MonoBehaviour
{

 public static bool plotted = false;
 public string inputdata;
 public static List<Dictionary<string, object>> pointList;
 public int columnStock = 0;
 public int columnX = 1;
 public int columnY = 2;
 public int columnZ = 3;
 public int columnSize = 4;
 public string stockName;
 public string xName;
 public string yName;
 public string zName;
 public string sizeName;
 public GameObject PointPrefab;
 public GameObject PointHolder;
 
 // Use this for initialization
    void Start () {
        //pointList = new List<Dictionary<string, object>>();
        // pointList = CSVReader.Read(inputdata);
        pointList = FirebaseReader.GetStocks();    

    }

 void Update() {
    if (pointList.Count != 0 && !plotted) {
        plotted = true;
        Debug.Log("num stocks: " + pointList.Count);

        foreach (Dictionary<string, object> stock in pointList.GetRange(0, Mathf.Clamp(pointList.Count, 0, 100))) {
            float x = Mathf.Clamp(System.Convert.ToSingle(stock["polarity"]) / 5f, 0, 25);
            float y =  Mathf.Clamp(System.Convert.ToSingle(stock["engagement"]) / 1f, 0, 25);
            float z =  Mathf.Clamp(System.Convert.ToSingle(stock["popularity"]) / 10000f, 0, 25);
            float size = Mathf.Clamp(System.Convert.ToSingle(stock["weight"]) / 10000f, 0, 500);

            GameObject dataPoint = Instantiate(PointPrefab, new Vector3(x, y, z), Quaternion.identity);
            dataPoint.transform.parent = PointHolder.transform;
            dataPoint.transform.name = (string) stock["title"];
            dataPoint.GetComponent<DataPt>().SetData(stock);
            dataPoint.GetComponent<Renderer>().material.color = new Color(x, y, z, 1.0f);
            dataPoint.GetComponent<Renderer>().material.SetColor("_Color", new Color(x, y, z, 1.0f));
            dataPoint.transform.localScale = new Vector3(size, size, size);
        }

        // List<string> columnList = new List<string>(pointList[1].Keys);
        
        // Debug.Log("There are " + columnList.Count + " columns in CSV");
        
        // foreach (string key in columnList)
        //     Debug.Log("Column name is " + key);

        // xName = columnList[columnX];
        // yName = columnList[columnY];
        // zName = columnList[columnZ];
        // stockName = columnList[columnStock];
        // sizeName = columnList[columnSize];

        // for (var i = 0; i < pointList.Count; i++)
        // {
        //     float x = System.Convert.ToSingle(pointList[i][xName]);
        //     float y = System.Convert.ToSingle(pointList[i][yName]);
        //     float z = System.Convert.ToSingle(pointList[i][zName]);
        //     string stock = pointList[i][stockName].ToString();
        //     float size = System.Convert.ToSingle(pointList[i][sizeName]);
            
        //     GameObject dataPoint = Instantiate(
        //     PointPrefab, 
        //     new Vector3(x, y, z), 
        //     Quaternion.identity);

        //     // dataPoint.transform.parent = PointHolder.transform;
        //     dataPoint.transform.name = stock;
        //     dataPoint.GetComponent<Renderer>().material.color = 
        //     new Color(x,y,z, 1.0f);
        //     dataPoint.transform.localScale = new Vector3(size,size,size);
        
        // }
     }
 }
 

}
