using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.iOS;
using UnityEngine.UI;

public class InputControl : MonoBehaviour
{
   public GameObject cameraOrbit;

   public GameObject slider;

   public float rotateSpeed = 8f;

   public float scrollFactor = 0f;

   void Update() {
        if (Input.GetMouseButton(0)) {
            float h = rotateSpeed * Input.GetAxis("Mouse X");
            float v = rotateSpeed * Input.GetAxis("Mouse Y");

            if (cameraOrbit.transform.eulerAngles.z + v <= 0.1f || cameraOrbit.transform.eulerAngles.z + v >= 179.9f) {
                    v = 0;
            }

            cameraOrbit.transform.eulerAngles = new Vector3(cameraOrbit.transform.eulerAngles.x, cameraOrbit.transform.eulerAngles.y + h, cameraOrbit.transform.eulerAngles.z + v);

            Ray ray = Camera.main.ScreenPointToRay (Input.mousePosition);
            RaycastHit hit;
            Debug.Log("Click");

            if (Physics.Raycast(ray, out hit, 100f) && hit.collider.gameObject.tag == "DataPt") {
                Debug.Log("Clicked data pt...");
                GameObject pt = hit.collider.gameObject;
                Dictionary<string, object> data = pt.GetComponent<DataPt>().GetData();
                UI.title = (string) data["title"];
                UI.polarity = System.Convert.ToSingle(data["polarity"]);
                UI.engagement = System.Convert.ToSingle(data["engagement"]);
                UI.popularity = System.Convert.ToSingle(data["popularity"]);
            } 
        } 

        // if (Input.touchCount >= 2) {
        //     Debug.Log("pinching...");
        //     Touch touchZero = Input.GetTouch(0);
        //     Touch touchOne = Input.GetTouch(1);

        //     Vector2 touchZeroPrevPos = touchZero.position - touchZero.deltaPosition;
        //     Vector2 touchOnePrevPos = touchOne.position - touchOne.deltaPosition;

        //     float prevMagnitude = (touchZeroPrevPos - touchOnePrevPos).magnitude;
        //     float currentMagnitude = (touchZero.position - touchOne.position).magnitude;

        //     float difference = currentMagnitude - prevMagnitude;

        //     scrollFactor = Mathf.Clamp(difference * 0.01f, 0, 1);
        // } else {
        //     scrollFactor = Input.GetAxis("Mouse ScrollWheel");
        // }

        scrollFactor = slider.GetComponent<Slider>().value;

       if (scrollFactor != 0) {
        //    cameraOrbit.transform.localScale = cameraOrbit.transform.localScale * (1f - scrollFactor);
        cameraOrbit.transform.localScale = new Vector3(1f, 1f, 1f) * (1f - scrollFactor);
       }

   }
}