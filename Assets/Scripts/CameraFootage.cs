using System.Collections;
using UnityEditor.PackageManager.Requests;
using UnityEngine;
using UnityEngine.UI;

public class CameraFootage : MonoBehaviour
{
    public WebCamTexture webcamTexture { get; private set; }
    public RawImage rawImage;
    public bool useFrontCamera = false;
    private bool hasCameraPermissions { get {
        #if UNITY_ANDROID
        return UnityEngine.Android.Permission.HasUserAuthorizedPermission(UnityEngine.Android.Permission.Camera);
        #elif UNITY_IOS
        return Application.HasUserAuthorization(UserAuthorization.WebCam);
        #else
        return true;
        #endif
    }}

    public void EnableCamera() {
        StartCoroutine(EnableCameraCoroutine());
    }

    IEnumerator EnableCameraCoroutine() {
        if (!hasCameraPermissions) yield return RequestCameraPermissions();

        if (hasCameraPermissions) InitializeCamera();
    }

    public void DisableCamera() {
        if (webcamTexture != null) {
            if (webcamTexture.isPlaying)
                webcamTexture.Stop();
            webcamTexture = null;
        }
    }

    
    IEnumerator RequestCameraPermissions()
    {
        #if UNITY_ANDROID
        if (!UnityEngine.Android.Permission.HasUserAuthorizedPermission(UnityEngine.Android.Permission.Camera))
        {
            UnityEngine.Android.Permission.RequestUserPermission(UnityEngine.Android.Permission.Camera);
            yield return new WaitForSeconds(1); // Wait for response (non-blocking)
        }
        #elif UNITY_IOS
        if (!Application.HasUserAuthorization(UserAuthorization.WebCam))
        {
            yield return Application.RequestUserAuthorization(UserAuthorization.WebCam);
        }
        #endif
    }

    void InitializeCamera()
    {
        WebCamDevice[] devices = WebCamTexture.devices;
        if (devices.Length == 0)
        {
            Debug.LogError("No cameras found");
            return;
        }

        string cameraName = null;
        foreach (var device in devices)
        {
            if (useFrontCamera ? device.isFrontFacing : !device.isFrontFacing)
            {
                cameraName = device.name;
                break;
            }
        }

        if (string.IsNullOrEmpty(cameraName))
            cameraName = devices[0].name;

        webcamTexture = new WebCamTexture(cameraName);
        rawImage.texture = webcamTexture;
        webcamTexture.Play();

        // Adjust orientation and aspect ratio
        StartCoroutine(AdjustCameraTexture());
    }

    IEnumerator AdjustCameraTexture()
    {
        yield return new WaitUntil(() => webcamTexture.width > 100);
        
        // Adjust aspect ratio
        float aspectRatio = (float)webcamTexture.width / webcamTexture.height;
        rawImage.rectTransform.localScale = new Vector3(rawImage.rectTransform.localScale.y, rawImage.rectTransform.localScale.y, 1);
        
        rawImage.rectTransform.sizeDelta = new Vector2(
            rawImage.rectTransform.rect.height * aspectRatio,
            rawImage.rectTransform.rect.height
        );
    }

    void OnDestroy()
    {
        if (webcamTexture != null && webcamTexture.isPlaying)
            webcamTexture.Stop();
    }
}
