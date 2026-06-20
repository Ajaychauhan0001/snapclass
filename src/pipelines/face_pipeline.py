import cv2
import numpy as np
import streamlit as st
from insightface.app import FaceAnalysis

from src.database.db import get_all_student


@st.cache_resource
def load_face_model():

    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"]
    )

    # Larger det_size = detector scans at higher resolution,
    # which is critical for group photos where individual
    # faces are small (e.g. 20+ students in one frame).
    app.prepare(
        ctx_id=0,
        det_size=(1280, 1280)
    )

    return app


def get_face_embedding(image_np):

    app = load_face_model()

    faces = app.get(image_np)

    embeddings = []

    for face in faces:
        embeddings.append(face.normed_embedding)

    return embeddings


def cosine_similarity(a, b):
    return float(np.dot(a, b))


def predict_attendance(class_image_np):

    # Resize only extremely large images (keep most resolution
    # so small/distant faces in group photos stay detectable)
    h, w = class_image_np.shape[:2]

    if w > 2400:
        scale = 2400 / w

        class_image_np = cv2.resize(
            class_image_np,
            None,
            fx=scale,
            fy=scale
        )

    detected_student = {}

    face_embeddings = get_face_embedding(
        class_image_np
    )

    students = get_all_student()

    if not students:
        return {}, [], len(face_embeddings)

    for face_embedding in face_embeddings:

        best_student = None
        best_score = -1

        for student in students:

            db_embedding = student.get(
                "face_embedding"
            )

            if not db_embedding:
                continue

            # db_embedding can be either:
            #   - a single embedding:  [0.1, 0.2, ...]
            #   - multiple embeddings: [[0.1, 0.2, ...], [0.15, 0.22, ...], ...]
            # Normalize it into a list of embeddings so both formats work.
            if isinstance(db_embedding[0], (list, tuple)):
                stored_embeddings = db_embedding
            else:
                stored_embeddings = [db_embedding]

            student_best_score = -1

            for stored_emb in stored_embeddings:

                stored_emb = np.array(
                    stored_emb,
                    dtype=np.float32
                )

                # Skip old Dlib embeddings / mismatched sizes
                if len(stored_emb) != len(face_embedding):
                    continue

                score = cosine_similarity(
                    face_embedding,
                    stored_emb
                )

                if score > student_best_score:
                    student_best_score = score

            if student_best_score > best_score:
                print(f"Student={student['name']} Score={student_best_score:.4f}")
                best_score = student_best_score
                best_student = student

        # Threshold
        if (
            best_student is not None
            and best_score >= 0.45
        ):
            detected_student[
                int(best_student["student_id"])
            ] = round(best_score, 3)

    all_students = [
        s["student_id"]
        for s in students
    ]

    return (
        detected_student,
        all_students,
        len(face_embeddings)
    )


def train_classifier():
    return True