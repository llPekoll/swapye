from django.urls import path

from .views import (
    BasicsDetailAPIview,
    CheckValidEmails,
    DateAPIView,
    DryRunAPIview,
    ExcellAPIView,
    ExcellSingleAPIView,
    ExtraRequestedDetailAPIView,
    ExtraRequestedListAPIView,
    GameDetailAPIview,
    GameIdentityAPIView,
    GameListAPIview,
    GameTypesAndSkinAPIView,
    PriceDetailAPIview,
    PriceListAPIview,
    RequestedAPIView,
    SocialMediaAPIView,
    EnableQrRecpetionAPIview,
    SalonModeAPIView,
    TimeFrameAPIview,
    FormsAPIView,
)
from .dropzoneCleanerViews import (
    BgInGameAPIView,
    FormLandScapeAPIView,
    FormPortraitAPIView,
    LogoDefaultAPIView,
    SoundDefaultAPIView,
    LogoAPIView,
    SoundAPIView,
)


urlpatterns = [
    path("games", GameListAPIview.as_view()),
    path("dash/<str:emblem>", GameDetailAPIview.as_view()),
    path("dash/<str:emblem>/price/<int:id>", PriceDetailAPIview.as_view()),
    path("dash/<str:emblem>/timeframe", TimeFrameAPIview.as_view()),
    path(
        "dash/<str:emblem>/prices/<str:type>", PriceListAPIview.as_view()
    ),  # /prices/game url will end up here
    path("dash/<str:emblem>/price/qr", EnableQrRecpetionAPIview.as_view()),
    path("dash/<str:emblem>/identity", GameIdentityAPIView.as_view()),
    path("dash/<str:emblem>/date", DateAPIView.as_view()),
    path("dash/<str:emblem>/forms", FormsAPIView.as_view()),
    path("dash/<str:emblem>/requested", RequestedAPIView.as_view()),
    path("dash/<str:emblem>/extrarequesteds", ExtraRequestedListAPIView.as_view()),
    path("dash/<str:emblem>/bgingame", BgInGameAPIView.as_view()),
    path("dash/<str:emblem>/formlandscape", FormLandScapeAPIView.as_view()),
    path("dash/<str:emblem>/formportrait", FormPortraitAPIView.as_view()),
    path("dash/defautls/logo", LogoDefaultAPIView.as_view()),
    path("dash/defautls/sound", SoundDefaultAPIView.as_view()),
    path("dash/<str:emblem>/sound", SoundAPIView.as_view()),
    path("dash/<str:emblem>/logo", LogoAPIView.as_view()),
    path(
        "dash/<str:emblem>/extrarequested/<int:id>",
        ExtraRequestedDetailAPIView.as_view(),
    ),
    path("dash/<str:emblem>/salon", SalonModeAPIView.as_view()),
    path("dash/<str:emblem>/socials", SocialMediaAPIView.as_view()),
    path("dash/<str:emblem>/dryrun", DryRunAPIview.as_view()),
    path("dash/<str:emblem>/basics", BasicsDetailAPIview.as_view()),
    path("gametypesnskins", GameTypesAndSkinAPIView.as_view()),
    path("export/<uuid:id>", ExcellAPIView.as_view()),
    path("export/<uuid:id>/<str:emblem>", ExcellSingleAPIView.as_view()),
    path("check/emails/<str:emblem>", CheckValidEmails.as_view()),
]
