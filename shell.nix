{ pkgs ? import <nixpkgs> { } }:

let 
  modpack_name = "otherwhere";
  webserver_host = "change_me";

  pack_url = "${webserver_host}/modpacks/${modpack_name}/pack.toml";

  memory_max = "5G";
  memory_min = "1G";
  java_package = pkgs.jre8;  

  install_server = pkgs.writeShellScriptBin "install_server" ''
    java -jar packwiz-installer-bootstrap.jar -g -s server ${pack_url}
    python forge_installer.py ${pack_url}
    mv *-universal.jar forge.jar
  '';

  run = pkgs.writeShellScriptBin "run" ''
    python check_eula.py
    java -jar packwiz-installer-bootstrap.jar -g -s server ${pack_url}
    java -Xms${memory_min} -Xmx${memory_max} -jar forge.jar
  '';

  diagnose_preprompt = ''
    You are a log file investigator
    You will receive a crash report from a modded minecraft server
    You should investigate this log file, reporting back with the name of the mod causing the problem, along with the lines you believe indicate this

    Sometimes, the offending mod will be labelled UE, this is an indication this mod has errored and it should be mentioned
    Likewise exceptions that appear to have been caused by a specific mod should be mentioned

    Respond concisely in bullet points, with only information you have been able to gather
  '';


  diagnose = pkgs.writeShellScriptBin "diagnose" ''
    ${pkgs.chatgpt-cli}/bin/chatgpt "${diagnose_preprompt} $(cat logs/latest.log)"
    

  '';
  
  runLoop = pkgs.writeShellScriptBin "run-loop" ''

    crashes=0
    while [ true ]
    do
      echo "Starting server..."
      run
      echo "Crashed! ($crashes crashes this run)"
      ((crashes++))
    done
  '';

in

pkgs.mkShell {
  buildInputs = [
    java_package
    run
    runLoop
    install_server
    diagnose
  ];
}
