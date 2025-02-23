using System;
using System.Collections;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Networking;

public class Capture : MonoBehaviour
{
    [Serializable]
    public class IngredientsResponse
    {
        public string[] ingredients;
    }

    public void CaptureContent() {
        CameraFootage cameraFootage = FindAnyObjectByType<CameraFootage>();

        Texture2D texture = new Texture2D(cameraFootage.rawImage.texture.width, cameraFootage.rawImage.texture.height);
        texture.SetPixels(cameraFootage.webcamTexture.GetPixels());
        texture.Apply();

        byte[] imageBytes = ImageConversion.EncodeToPNG(texture);
        string base64String = Convert.ToBase64String(imageBytes);

        cameraFootage.DisableCamera();

        StartCoroutine(Upload(base64String));
    }

    IEnumerator Upload(string image) {
        using (UnityWebRequest www = UnityWebRequest.Post("https://my-service-894665829957.us-central1.run.app/get_ingredients",
                                                          $"{{\"image\": \"{image}\"}}", "application/json"))
        {
            Debug.Log(System.Text.Encoding.UTF8.GetString(www.uploadHandler.data));
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.downloadHandler.text);
            }
            else
            {
                var responseText = $"{{\"ingredients\": {www.downloadHandler.text}}}";
                Debug.Log(responseText);

                string[] ingredients = JsonUtility.FromJson<IngredientsResponse>(responseText).ingredients;
                AddIngredient addIngredient = FindAnyObjectByType<AddIngredient>();
                foreach (string ingredient in ingredients)
                {
                    addIngredient.Add(ingredient);
                }
            }
        }
    }
}
