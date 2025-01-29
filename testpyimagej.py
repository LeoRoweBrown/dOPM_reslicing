import imagej, scyjava

def test_pyimagej():
    
    memory_gb = 50
    scyjava.config.add_option(f"-Xmx{memory_gb}g")
    mode = 'interactive'
    mode = 'gui'
    
    download_imagej = True
    imagej_dir = "A:/leo_imagej/fiji-win64/fiji-win64/Fiji.app"
    imagej_dir = "C:/Users/lnr19/OneDrive - Imperial College London/postdoc_2024/fiji-win64/Fiji.app/"
    
    if 'ij' not in globals():
        # ij = imagej.init('sc.fiji:fiji:2.14.0')
        if download_imagej:
            print("Downloading ImageJ")
            # ij = imagej.init(['sc.fiji:fiji:2.16.0', 'net.preibisch:BigStitcher:2.3.1', 'net.preibisch:multiview-reconstruction:4.3.6'], mode=mode)
            ij = imagej.init(['sc.fiji:fiji:2.16.0', 'net.preibisch:BigStitcher:2.3.1', 'net.preibisch:multiview-reconstruction:5.0.3'], mode=mode)
    
            # ij = imagej.init('net.preibisch:BigStitcher:2.2.1', mode=mode)
    
        elif imagej_dir is not None:
            print(f"Opening ImageJ from {imagej_dir}")
            ij = imagej.init(imagej_dir, mode=mode)
        else:
            raise FileNotFoundError("No imageJ dir given, use download ImageJ=True")
        print("Created ImageJ instance", ij.getVersion()) 
    else:
        print(f"ImageJ instance already exists ({ij.getVersion()})")
