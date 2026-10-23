from vector import cylinder_force, format_reactions_report
from models.max250 import build_max250
from configs.prj175 import cases


def analyse_config(case_label, case):
    machine = build_max250(**case)
    reactions = machine.reactions()
    cylinder_result = cylinder_force(reactions)

    print(format_reactions_report(reactions, case_label=case_label, case_params=case,
                                   cylinder_result=cylinder_result))
    print()

    return case_label, case, reactions, cylinder_result


if __name__ == '__main__':
    results = [analyse_config(f"Case {number}", case) for number, case in enumerate(cases, start=1)]

    print("=== Summary across all cases ===")
    for case_label, case, reactions, cylinder_result in results:
        print(f"{case_label:<8} mast_angle={case['mast_angle']:>6}  holdback={case['holdback']:>8}  "
              f"total moment.z={reactions['moments'].z:>12.2f}  cylinder force={cylinder_result['force']:>10.2f}"
              f"  lever={cylinder_result['lever']:>7.2f}")
