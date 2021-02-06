using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DataPt : MonoBehaviour
{
    Dictionary<string, object> data = new Dictionary<string, object>();
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public Dictionary<string, object> GetData() {
        return data;
    }

    public void SetData(Dictionary<string, object> dict) {
        data = dict;
    }


}
