using UnityEngine;
using System.Collections;
 
public class CameraController : MonoBehaviour
{
   public Transform cameraOrbit;
   public Transform target;

   void Start()
   {
       cameraOrbit.position = target.position;
   }

   void Update()
   {
       transform.rotation = Quaternion.Euler(transform.rotation.x, transform.rotation.y, 0);

       transform.LookAt(target.position);
   }
}