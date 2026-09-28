package com.nexavideo.video

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

// PDF Feature 3: Shorts API + Navigation
// PDF Feature 4: Video Upload MVP
// PDF Feature 5: Likes / Follows

@Composable
fun VideoPlayer(
    videoUrl: String,
    title: String,
    onLike: () -> Unit
) {
    var liked by remember { mutableStateOf(false) }
    
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        // Video Placeholder (MVP me local player)
        Card(modifier = Modifier.fillMaxWidth().height(300.dp)) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                Text("▶ Playing: $title")
            }
        }
        
        Spacer(modifier = Modifier.height(12.dp))
        Text(title, style = MaterialTheme.typography.titleMedium)
        
        Row {
            Button(onClick = { 
                liked = !liked
                onLike()
            }) {
                Text(if(liked) "❤️ Liked" else "🤍 Like")
            }
            Spacer(modifier = Modifier.width(8.dp))
            Button(onClick = { /* Follow API call */ }) {
                Text("Follow")
            }
        }
        
        // Backend API Call Info
        Text(
            "API: POST /api/social/like & /api/shorts",
            style = MaterialTheme.typography.labelSmall
        )
    }
}

@Composable
fun ShortsFeedScreen(videos: List<String>) {
    Column {
        Text("Shorts Feed - PDF Feature 3 ✅")
        videos.forEach { url ->
            VideoPlayer(videoUrl = url, title = "Short Video", onLike = {})
        }
    }
}
