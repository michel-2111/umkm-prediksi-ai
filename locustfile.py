from locust import HttpUser, task, between

class SimulasiPenggunaUMKM(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def buka_halaman_utama(self):
        """Menyimulasikan UMKM membuka halaman dashboard utama"""
        self.client.get("/")

    @task(1)
    def cek_kesehatan_server(self):
        """Menyimulasikan pengecekan status server Streamlit di latar belakang"""
        self.client.get("/_stcore/health")