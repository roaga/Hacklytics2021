using UnityEngine;
using System.Collections;
using UnityEngine.iOS;

public class InputControl : MonoBehaviour
{
   public GameObject cameraOrbit;

   public float rotateSpeed = 8f;

   void Update() {
        if (Input.GetMouseButton(0) || Input.touchCount == 1) {
            Debug.Log("dragging...");
            float h = rotateSpeed * Input.GetAxis("Mouse X");
            float v = rotateSpeed * Input.GetAxis("Mouse Y");

            if (cameraOrbit.transform.eulerAngles.z + v <= 0.1f || cameraOrbit.transform.eulerAngles.z + v >= 179.9f) {
                    v = 0;
            }

            cameraOrbit.transform.eulerAngles = new Vector3(cameraOrbit.transform.eulerAngles.x, cameraOrbit.transform.eulerAngles.y + h, cameraOrbit.transform.eulerAngles.z + v);
        } 

        float scrollFactor; 
        if (Input.touchCount >= 2) {
            Debug.Log("pinching...");
            Touch touchZero = Input.GetTouch(0);
            Touch touchOne = Input.GetTouch(1);

            Vector2 touchZeroPrevPos = touchZero.position - touchZero.deltaPosition;
            Vector2 touchOnePrevPos = touchOne.position - touchOne.deltaPosition;

            float prevMagnitude = (touchZeroPrevPos - touchOnePrevPos).magnitude;
            float currentMagnitude = (touchZero.position - touchOne.position).magnitude;

            float difference = currentMagnitude - prevMagnitude;

            scrollFactor = Mathf.Clamp(difference * 0.01f, 0, 1);
        } else {
            scrollFactor = Input.GetAxis("Mouse ScrollWheel");
        }

       if (scrollFactor != 0) {
           cameraOrbit.transform.localScale = cameraOrbit.transform.localScale * (1f - scrollFactor);
       }

   }
}