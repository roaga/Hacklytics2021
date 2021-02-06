using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Firebase.Firestore;
using Firebase.Extensions;

public class FirebaseReader
{
    static FirebaseFirestore db = FirebaseFirestore.DefaultInstance;
    static CollectionReference stocksRef = db.Collection("stocks");

    static List<Dictionary<string, object>> stocks = new List<Dictionary<string, object>>();

    public static List<Dictionary<string, object>> GetStocks() {
        var res = stocksRef.GetSnapshotAsync().ContinueWithOnMainThread(task => {
            QuerySnapshot snapshot = task.Result;
            foreach (DocumentSnapshot doc in snapshot.Documents) {
                Dictionary<string, object> docDictionary = doc.ToDictionary();
                stocks.Add(docDictionary);
            }
            DataPlot.pointList = stocks;
            DataPlot.plotted = false;
        });

        return stocks;
    }
}
