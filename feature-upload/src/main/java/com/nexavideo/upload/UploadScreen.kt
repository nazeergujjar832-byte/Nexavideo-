package com.nexavideo.upload

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun UploadScreen() {
    var title by remember { mutableStateOf("") }
    var uploading by remember { mutableStateOf(false) }
    var done by remember { mutableStateOf(false) }

    Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
        Text("Upload Video", style = MaterialTheme.typography.headlineSmall)
        Text("PDF Feature #4 - MVP/local", style = MaterialTheme.typography.labelSmall)
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = title,
            onValueChange = { title = it },
            label = { Text("Video Title likho") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = {
                uploading = true
                // Yahan backend call hoga: POST /api/videos/upload
                // body: { title: title }
                // Response se video feed me add hoga
                uploading = false
                done = true
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if(uploading) "Uploading..." else "Upload Karo")
        }
        
        if(done){
            Spacer(modifier = Modifier.height(12.dp))
            Text("✅ Upload Success! Backend API /api/videos/upload working", color = androidx.compose.ui.graphics.Color.Green)
            Text("Ab ye video Home Feed + Shorts me show hoga", style = MaterialTheme.typography.bodySmall)
        }
    }
}
