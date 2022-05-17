/***************************************************************
 * Name:      wxWidgetsApp.cpp
 * Purpose:   Code for Application Class
 * Author:    Holger Lech ()
 * Created:   2022-05-17
 * Copyright: Holger Lech ()
 * License:
 **************************************************************/

#ifdef WX_PRECOMP
#include "wx_pch.h"
#endif

#ifdef __BORLANDC__
#pragma hdrstop
#endif //__BORLANDC__

#include "wxWidgetsApp.h"
#include "wxWidgetsMain.h"

IMPLEMENT_APP(wxWidgetsApp);

bool wxWidgetsApp::OnInit()
{
    wxWidgetsFrame* frame = new wxWidgetsFrame(0L, _("wxWidgets Application Template"));
    frame->SetIcon(wxICON(aaaa)); // To Set App Icon
    frame->Show();
    
    return true;
}
