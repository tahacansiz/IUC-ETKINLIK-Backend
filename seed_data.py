"""
Seed script to populate the MySQL database with sample data
Run with: python seed_data.py
"""

import asyncio
import uuid
from datetime import datetime, timedelta

# Add app to path
import sys
sys.path.insert(0, '.')

from app.core.database import AsyncSessionLocal, init_db
from app.core.security import hash_password
from app.models.user import User
from app.models.category import Category
from app.models.event import Event
from app.models.event_participant import EventParticipant


async def seed_database():
    """Seed the database with sample data"""
    
    # Initialize database
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        from sqlalchemy import select, delete
        
        # Clear existing data first
        print("🗑️ Clearing existing data...")
        await session.execute(delete(EventParticipant))
        await session.execute(delete(Event))
        await session.execute(delete(Category))
        await session.execute(delete(User))
        await session.commit()
        
        print("🌱 Seeding database...")
        
        # ==================== CATEGORIES ====================
        categories = [
            Category(
                id=str(uuid.uuid4()),
                name="Teknoloji",
                icon_name="computer",
                color_hex="#2196F3"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Spor",
                icon_name="sports_soccer",
                color_hex="#4CAF50"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Müzik",
                icon_name="music_note",
                color_hex="#9C27B0"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Sanat",
                icon_name="palette",
                color_hex="#FF9800"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Eğitim",
                icon_name="school",
                color_hex="#607D8B"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Kariyer",
                icon_name="work",
                color_hex="#795548"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Sosyal",
                icon_name="groups",
                color_hex="#E91E63"
            ),
            Category(
                id=str(uuid.uuid4()),
                name="Kültür",
                icon_name="theater_comedy",
                color_hex="#00BCD4"
            ),
        ]
        
        for cat in categories:
            session.add(cat)
        await session.flush()
        print(f"✅ {len(categories)} kategori eklendi")
        
        # ==================== USERS ====================
        # Admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            full_name="Admin User",
            email="admin@iuc.edu.tr",
            hashed_password=hash_password("admin123"),
            role="admin",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(admin_user)
        
        # Club Admin users
        club_admin1 = User(
            id=str(uuid.uuid4()),
            full_name="Bilişim Kulübü",
            email="bilisim@iuc.edu.tr",
            hashed_password=hash_password("club123"),
            role="clubAdmin",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(club_admin1)
        
        club_admin2 = User(
            id=str(uuid.uuid4()),
            full_name="Müzik Kulübü",
            email="muzik@iuc.edu.tr",
            hashed_password=hash_password("club123"),
            role="clubAdmin",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(club_admin2)
        
        club_admin3 = User(
            id=str(uuid.uuid4()),
            full_name="Spor Kulübü",
            email="spor@iuc.edu.tr",
            hashed_password=hash_password("club123"),
            role="clubAdmin",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(club_admin3)
        
        # Student users
        student1 = User(
            id=str(uuid.uuid4()),
            full_name="Ahmet Yılmaz",
            email="ahmet@iuc.edu.tr",
            hashed_password=hash_password("student123"),
            role="student",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(student1)
        
        student2 = User(
            id=str(uuid.uuid4()),
            full_name="Ayşe Demir",
            email="ayse@iuc.edu.tr",
            hashed_password=hash_password("student123"),
            role="student",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(student2)
        
        student3 = User(
            id=str(uuid.uuid4()),
            full_name="Mehmet Kaya",
            email="mehmet@iuc.edu.tr",
            hashed_password=hash_password("student123"),
            role="student",
            is_active=True,
            avatar_url=None,
            created_at=datetime.utcnow()
        )
        session.add(student3)
        
        await session.flush()
        print("✅ 7 kullanıcı eklendi")
        
        # ==================== EVENTS ====================
        now = datetime.utcnow()
        
        # Unsplash image URLs for events
        images = {
            'ai': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop',
            'football': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&h=600&fit=crop',
            'career': 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&h=600&fit=crop',
            'theater': 'https://images.unsplash.com/photo-1503095396549-807759245b35?w=800&h=600&fit=crop',
            'sports': 'https://images.unsplash.com/photo-1461896836934- voices40e54a?w=800&h=600&fit=crop',
            'guitar': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800&h=600&fit=crop',
            'web': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&h=600&fit=crop',
            'photo': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800&h=600&fit=crop',
            'basketball': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800&h=600&fit=crop',
            'startup': 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=600&fit=crop',
            'art': 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&h=600&fit=crop',
            'yoga': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop',
            'hackathon': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=600&fit=crop',
            'cinema': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&h=600&fit=crop',
            'chess': 'https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=800&h=600&fit=crop',
            'music': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop',
            'social': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800&h=600&fit=crop',
            'conference': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=600&fit=crop',
        }
        
        events = [
            # FEATURED EVENTS (is_featured=True)
            Event(
                id=str(uuid.uuid4()),
                title="Yapay Zeka Workshop",
                description="Yapay zeka ve makine öğrenmesi hakkında uygulamalı workshop. Python ile temel AI kavramlarını öğreneceksiniz. Katılımcılara sertifika verilecektir.",
                event_date=now + timedelta(days=7),
                location="Bilgisayar Mühendisliği Lab 1",
                image_url=images['ai'],
                category_id=categories[0].id,  # Teknoloji
                status="upcoming",
                creator_id=club_admin1.id,
                organizer_name="Bilişim Kulübü",
                max_participants=50,
                current_participants=12,
                is_featured=True,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Üniversiteler Arası Futbol Turnuvası",
                description="İstanbul üniversiteleri arası futbol turnuvası. Takımlar halinde katılım sağlanacaktır. Kazanan takıma kupa ve madalya verilecektir.",
                event_date=now + timedelta(days=14),
                location="Spor Sahası",
                image_url=images['football'],
                category_id=categories[1].id,  # Spor
                status="upcoming",
                creator_id=club_admin3.id,
                organizer_name="Spor Kulübü",
                max_participants=200,
                current_participants=85,
                is_featured=True,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Kariyer Günleri 2026",
                description="Sektörün önde gelen firmalarıyla tanışma fırsatı. CV hazırlama workshopları ve birebir görüşmeler yapılacaktır.",
                event_date=now + timedelta(days=21),
                location="Kongre Merkezi",
                image_url=images['career'],
                category_id=categories[5].id,  # Kariyer
                status="upcoming",
                creator_id=admin_user.id,
                organizer_name="Kariyer Merkezi",
                max_participants=500,
                current_participants=234,
                is_featured=True,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Tiyatro Gösterisi: Hamlet",
                description="Shakespeare'in ölümsüz eseri Hamlet'in sahnelenişi. Tiyatro kulübü öğrencileri tarafından sergilenecektir.",
                event_date=now + timedelta(days=8),
                location="Konferans Salonu",
                image_url=images['theater'],
                category_id=categories[7].id,  # Kültür
                status="upcoming",
                creator_id=admin_user.id,
                organizer_name="Tiyatro Kulübü",
                max_participants=150,
                current_participants=89,
                is_featured=True,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Kış Spor Festivali",
                description="Bir hafta sürecek spor etkinlikleri festivali. Voleybol, basketbol ve masa tenisi turnuvaları.",
                event_date=now + timedelta(days=1),
                location="Kampüs Geneli",
                image_url=images['basketball'],
                category_id=categories[1].id,  # Spor
                status="upcoming",
                creator_id=club_admin3.id,
                organizer_name="Spor Kulübü",
                max_participants=300,
                current_participants=267,
                is_featured=True,
                created_at=now - timedelta(days=5)
            ),
            
            # REGULAR EVENTS (is_featured=False)
            Event(
                id=str(uuid.uuid4()),
                title="Akustik Gitar Gecesi",
                description="Akustik gitar performansları ve jam session. Kendi gitarınızı getirip sahneye çıkabilirsiniz.",
                event_date=now + timedelta(days=5),
                location="Öğrenci Merkezi Sahne",
                image_url=images['guitar'],
                category_id=categories[2].id,  # Müzik
                status="upcoming",
                creator_id=club_admin2.id,
                organizer_name="Müzik Kulübü",
                max_participants=100,
                current_participants=45,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Web Geliştirme Bootcamp",
                description="3 günlük yoğun web geliştirme eğitimi. HTML, CSS, JavaScript ve React öğreneceksiniz.",
                event_date=now + timedelta(days=10),
                location="Bilgisayar Lab 3",
                image_url=images['web'],
                category_id=categories[0].id,  # Teknoloji
                status="upcoming",
                creator_id=club_admin1.id,
                organizer_name="Bilişim Kulübü",
                max_participants=30,
                current_participants=28,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Fotoğrafçılık Atölyesi",
                description="Temel fotoğrafçılık teknikleri ve kompozisyon kuralları. DSLR veya aynasız kamera ile katılım önerilir.",
                event_date=now + timedelta(days=3),
                location="Sanat Galerisi",
                image_url=images['photo'],
                category_id=categories[3].id,  # Sanat
                status="upcoming",
                creator_id=club_admin2.id,
                organizer_name="Fotoğrafçılık Kulübü",
                max_participants=25,
                current_participants=18,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Basketbol Turnuvası",
                description="Fakülteler arası basketbol turnuvası. 5 kişilik takımlar halinde kayıt olunabilir.",
                event_date=now + timedelta(days=12),
                location="Kapalı Spor Salonu",
                image_url=images['basketball'],
                category_id=categories[1].id,  # Spor
                status="upcoming",
                creator_id=club_admin3.id,
                organizer_name="Spor Kulübü",
                max_participants=80,
                current_participants=56,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Girişimcilik Söyleşisi",
                description="Başarılı girişimcilerle söyleşi ve networking etkinliği. Startup ekosistemi hakkında bilgi edinme fırsatı.",
                event_date=now + timedelta(days=15),
                location="İşletme Fakültesi Amfi",
                image_url=images['startup'],
                category_id=categories[5].id,  # Kariyer
                status="upcoming",
                creator_id=admin_user.id,
                organizer_name="Girişimcilik Kulübü",
                max_participants=200,
                current_participants=145,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Resim Sergisi Açılışı",
                description="Öğrenci resim sergisi açılışı. Farklı tekniklerle hazırlanmış eserler sergilenecektir.",
                event_date=now + timedelta(days=2),
                location="Ana Bina Sergi Salonu",
                image_url=images['art'],
                category_id=categories[3].id,  # Sanat
                status="upcoming",
                creator_id=club_admin2.id,
                organizer_name="Güzel Sanatlar Kulübü",
                max_participants=100,
                current_participants=34,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Python ile Veri Analizi",
                description="Python ve Pandas kütüphanesi ile veri analizi temelleri. Gerçek veri setleri üzerinde çalışacağız.",
                event_date=now + timedelta(days=18),
                location="Bilgisayar Lab 2",
                image_url=images['web'],
                category_id=categories[0].id,  # Teknoloji
                status="upcoming",
                creator_id=club_admin1.id,
                organizer_name="Bilişim Kulübü",
                max_participants=40,
                current_participants=35,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Klasik Müzik Konseri",
                description="Üniversite orkestrası tarafından Beethoven ve Mozart eserleri seslendirilecektir.",
                event_date=now + timedelta(days=9),
                location="Büyük Konferans Salonu",
                image_url=images['music'],
                category_id=categories[2].id,  # Müzik
                status="upcoming",
                creator_id=club_admin2.id,
                organizer_name="Müzik Kulübü",
                max_participants=250,
                current_participants=180,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Satranç Turnuvası",
                description="Açık satranç turnuvası. Her seviyeden katılımcı kabul edilmektedir.",
                event_date=now + timedelta(days=6),
                location="Öğrenci Merkezi",
                image_url=images['chess'],
                category_id=categories[6].id,  # Sosyal
                status="upcoming",
                creator_id=admin_user.id,
                organizer_name="Satranç Kulübü",
                max_participants=64,
                current_participants=48,
                is_featured=False,
                created_at=now
            ),
            Event(
                id=str(uuid.uuid4()),
                title="İngilizce Konuşma Kulübü",
                description="Her hafta farklı konularda İngilizce pratik yapma etkinliği. Tüm seviyeler katılabilir.",
                event_date=now + timedelta(days=4),
                location="Dil Merkezi",
                image_url=images['conference'],
                category_id=categories[4].id,  # Eğitim
                status="upcoming",
                creator_id=admin_user.id,
                organizer_name="Dil Kulübü",
                max_participants=30,
                current_participants=22,
                is_featured=False,
                created_at=now
            ),
            
            # COMPLETED EVENTS
            Event(
                id=str(uuid.uuid4()),
                title="Hackathon 2025",
                description="24 saatlik kod maratonu. Takımlar halinde projeler geliştirildi.",
                event_date=now - timedelta(days=30),
                location="Mühendislik Fakültesi",
                image_url=images['hackathon'],
                category_id=categories[0].id,  # Teknoloji
                status="completed",
                creator_id=club_admin1.id,
                organizer_name="Bilişim Kulübü",
                max_participants=100,
                current_participants=100,
                is_featured=False,
                created_at=now - timedelta(days=60)
            ),
            Event(
                id=str(uuid.uuid4()),
                title="Yılbaşı Konseri",
                description="Yılbaşı özel müzik gecesi.",
                event_date=now - timedelta(days=12),
                location="Ana Salon",
                image_url=images['music'],
                category_id=categories[2].id,  # Müzik
                status="completed",
                creator_id=club_admin2.id,
                organizer_name="Müzik Kulübü",
                max_participants=300,
                current_participants=285,
                is_featured=False,
                created_at=now - timedelta(days=40)
            ),
            
            # ONGOING EVENT
            Event(
                id=str(uuid.uuid4()),
                title="Fotoğraf Yarışması",
                description="Kampüs temalı fotoğraf yarışması. Eserler toplanıyor.",
                event_date=now - timedelta(days=2),
                location="Online",
                image_url=images['photo'],
                category_id=categories[3].id,  # Sanat
                status="ongoing",
                creator_id=club_admin2.id,
                organizer_name="Fotoğrafçılık Kulübü",
                max_participants=200,
                current_participants=156,
                is_featured=False,
                created_at=now - timedelta(days=15)
            ),
        ]
        
        for event in events:
            session.add(event)
        await session.flush()
        print(f"✅ {len(events)} etkinlik eklendi ({sum(1 for e in events if e.is_featured)} öne çıkan)")
        
        # ==================== EVENT PARTICIPANTS ====================
        # Add some participants to events
        participations = [
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student1.id,
                event_id=events[0].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student2.id,
                event_id=events[0].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student3.id,
                event_id=events[0].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student1.id,
                event_id=events[1].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student2.id,
                event_id=events[2].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student3.id,
                event_id=events[3].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student1.id,
                event_id=events[5].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student2.id,
                event_id=events[6].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student3.id,
                event_id=events[7].id
            ),
            EventParticipant(
                id=str(uuid.uuid4()),
                user_id=student1.id,
                event_id=events[8].id
            ),
        ]
        
        for participation in participations:
            session.add(participation)
        
        await session.commit()
        print(f"✅ {len(participations)} katılım kaydı eklendi")
        
        print("\n🎉 Veritabanı başarıyla dolduruldu!")
        print("\n📋 Test Hesapları:")
        print("=" * 50)
        print("Admin:      admin@iuc.edu.tr / admin123")
        print("Kulüp 1:    bilisim@iuc.edu.tr / club123")
        print("Kulüp 2:    muzik@iuc.edu.tr / club123")
        print("Kulüp 3:    spor@iuc.edu.tr / club123")
        print("Öğrenci 1:  ahmet@iuc.edu.tr / student123")
        print("Öğrenci 2:  ayse@iuc.edu.tr / student123")
        print("Öğrenci 3:  mehmet@iuc.edu.tr / student123")
        print("=" * 50)
        print("\n📊 Özet:")
        print(f"   - {len(categories)} kategori")
        print(f"   - 7 kullanıcı (1 admin, 3 kulüp, 3 öğrenci)")
        print(f"   - {len(events)} etkinlik (5 öne çıkan)")
        print(f"   - {len(participations)} katılım kaydı")


if __name__ == "__main__":
    asyncio.run(seed_database())
