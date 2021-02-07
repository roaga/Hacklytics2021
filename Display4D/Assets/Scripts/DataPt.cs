using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DataPt : MonoBehaviour
{
    Dictionary<string, object> data = new Dictionary<string, object>();

    public Material material1;
    public Material material2;
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (UI.title == (string) data["title"]) {
            gameObject.GetComponent<MeshRenderer>().material = material2;
        } else {
            gameObject.GetComponent<MeshRenderer>().material = material1;
        }
    }

    public Dictionary<string, object> GetData() {
        return data;
    }

    public void SetData(Dictionary<string, object> dict) {
        data = dict;
    }


}
