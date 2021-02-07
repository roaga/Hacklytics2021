using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class UI : MonoBehaviour
{
    public static string title = "";
    float polarity = 0f;
    float popularity = 0f;
    float engagement = 0f;

    public TMPro.TextMeshProUGUI titleText;
    public TMPro.TextMeshProUGUI polarityText;
    public TMPro.TextMeshProUGUI popularityText;
    public TMPro.TextMeshProUGUI engagementText;


    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        titleText.text = title;
        polarityText.text = "Sentiment Strength: " + polarity.ToString();
        popularityText.text = "Popularity: " + popularity.ToString();
        engagementText.text = "Engagement: " + engagement.ToString();
    }

    void OnMouseDown() {
        Ray ray = Camera.main.ScreenPointToRay (Input.mousePosition);
        RaycastHit hit;
        Debug.Log("Click");

        if (Physics.Raycast(ray, out hit, 100f) && hit.collider.gameObject.tag == "DataPt") {
            Debug.Log("Clicked data pt...");
            GameObject pt = hit.collider.gameObject;
            Dictionary<string, object> data = pt.GetComponent<DataPt>().GetData();
            title = (string) data["title"];
            polarity = System.Convert.ToSingle(data["polarity"]);
            engagement = System.Convert.ToSingle(data["engagement"]);
            popularity = System.Convert.ToSingle(data["popularity"]);
        } 
    }
}
